#! /usr/bin/env python
import sys
import operator
import json
from harpoon.commands.base import Command
from harpoon.lib.robtex import Robtex, RobtexError
from harpoon.lib.utils import json_serial
from datetime import date, datetime

class CommandRobtex(Command):
    name = "robtex"
    description = "Search in Robtex API (https://www.robtex.com/api/)"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(help='Subcommand')
        parser_a = subparsers.add_parser('ip', help='Request info on an IP')
        parser_a.add_argument('IP',  help='IP')
        parser_a.add_argument('--json', '-j', action='store_true', help='Show raw JSON info')
        parser_a.set_defaults(subcommand='ip')
        parser_b = subparsers.add_parser('asn', help='Request info on an ASN')
        parser_b.add_argument('ASN',  help='ASN', type=int)
        parser_b.add_argument('--json', '-j', action='store_true', help='Show raw JSON info')
        parser_b.set_defaults(subcommand='asn')
        parser_c = subparsers.add_parser('domain', help='Request info on a domain')
        parser_c.add_argument('DOMAIN',  help='DOMAIN')
        parser_c.add_argument('--json', '-j', action='store_true', help='Show raw JSON info')
        parser_c.set_defaults(subcommand='domain')
        self.parser = parser

    def run(self, conf, args):
        if 'subcommand' in args:
            if args.subcommand == "ip":
                r = Robtex()
                res = r.get_ip_info(args.IP)
                if args.json:
                    print(json.dumps(res, sort_keys=True, indent=4, default=json_serial))
                else:
                    print("AS %i: %s" % (res["as"], res["asname"]))
                    print("Location: %s, %s" % (res["city"], res["country"]))
                    print("BGP Route: %s, %s" % (res["bgproute"], res["routedesc"]))
                    print("Whois: %s" % res["whoisdesc"])
                    print("https://www.robtex.com/ip-lookup/%s" % args.IP)
                    if "pas" in res:
                        if len(res["pas"]):
                            print("Passive DNS:")
                            for d in res["pas"]:
                                print("\t%s %s" % (d["date"].isoformat(), d["o"]))
                    if "pash" in res:
                        if len(res["pash"]):
                            print("Passive DNS History:")
                            for d in res["pash"]:
                                print("\t%s %s" % (d["date"].isoformat(), d["o"]))
                    if "act" in res:
                        if len(res["act"]):
                            print("Active DNS:")
                            for d in res["act"]:
                                print("\t%s %s" % (d["date"].isoformat(), d["o"]))
                    if "acth" in res:
                        if len(res["acth"]):
                            print("ACtive DNS History:")
                            for d in res["acth"]:
                                print("\t%s %s" % (d["date"].isoformat(), d["o"]))
            elif args.subcommand == "asn":
                r = Robtex()
                res = r.get_asn_info(args.ASN)
                if args.json:
                    print(json.dumps(res, sort_keys=True, indent=4, default=json_serial))
                else:
                    print("ASN Routes:")
                    for n in res["nets"]:
                        print("[+] %s" % n["n"])
            elif args.subcommand == "domain":
                r = Robtex()
                res = r.get_pdns_domain(args.DOMAIN)
                if args.json:
                    print(json.dumps(res, sort_keys=True, indent=4, default=json_serial))
                else:
                    if len(res) == 0:
                        print("No information on this domain")
                    else:
                        print("Passive DNS info:")
                        for r in res:
                            print("[+] %s\t%s\t(%s -> %s)" % (
                                    r["rrtype"],
                                    r["rrdata"],
                                    r["time_first_o"].isoformat(),
                                    r["time_last_o"].isoformat()
                                )
                            )
            else:
                self.parser.print_help()
        else:
            self.parser.print_help()
