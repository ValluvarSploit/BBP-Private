#!/usr/bin/python
#
# import masscan output and run an nmap scan on the results
#

import sys
import argparse

from libnmap.parser import NmapParser, NmapParserException
from libnmap.process import NmapProcess
from collections import defaultdict
from time import sleep

parser = argparse.ArgumentParser(description='Import masscan results and run an nmap scan against the target.')
parser.add_argument('f' --scan-file, dest='scan_file', help='Masscan XML file')
#parser.add_argument('-f', '--scan_file', nargs='?', type=argparse.FileType('r'), help='XML file containing masscan results.')
args = parser.parse_args()

def do_scan(target, options):

    nmproc = NmapProcess(target, options)
    rc = nmproc.sudo_run_background()

    while nmproc.is_running():
        print("Nmap scan running: ETC: {0} DONE: {1}%".format(nmproc.etc,nmproc.progress))
        sleep(2)

    if (rc !=0):
        print("Nmap scan failed: {0}".format(nmproc.stderr))
    
    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Scan parsing failed: {0}".format(e.msg))

    print("rc: {0} output: {1}".format(nmproc.rc, nmproc.summary))
    return parsed

def main():
    
    # space on the end is on purpose
    options = "-sS -sV -O -sC -p "

    try:
        report = NmapParser.parse_fromfile(args.scan_file)
    except NmapParserException as e:
        print("Scan parsing failed: {0}".format(nmproc.stderr))

    report_dict = defaultdict(list)
    for host in report.hosts:
        for service in host.services:
            report_dict[host.ipv4].append(service.port)

    for target, ports in report_dict.items():
        print("Getting ready to scan {0} on ports {1}".format(target, ', '.join(map(str, ports))))
        do_scan(target, options)

if __name__ == '__main__':
    main()
