#!/usr/bin/env python3

#import argparse
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from time import sleep, strftime, localtime
from collections import defaultdict

#parser = argparse.ArgumentParser(description='Import masscan results and run an nmap scan against the target.')
#parser.add_argument('-f', '--scan_file', nargs='?', type=argparse.FileType('r'))
#args = parser.parse_args()

def do_scan(target, options):
    parsed = None
    nmproc = NmapProcess(target, options)
    rc = nmproc.run()
    
    while nmproc.is_running():
        print('Nmap scan running: ETC: {0} DONE: {1}%'.format(nmproc.etc, nmproc.progress))
        sleep(10)

    if nmproc.rc != 0:
        print('nmap scan failed: {0}'.format(nmproc.stderr))
    
    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print('Scan parsing failed: {0}'.format(e.msg))

    return parsed

def print_scan(nmap_report):
    print('Starting Nmap {0} ( http:nmap.org ) at {1}'.format(
        nmap_report.version, 
        strftime('%d-%m-%Y %H:%M', localtime(int(nmap_report.started)))))
    
    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print('Nmap scan report for {0} ({1})'.format(
            tmp_host, 
            host.address))
        print('Host is {0}.'.format(host.status))
        print('  PORT     STATE         SERVICE')

        for serv in host.services:
            pserv = '{0:>5s}/{1:3s}  {2:12s}  {3}'.format(
                str(serv.port),
                serv.protocol,
                serv.state,
                serv.service)
            if len(serv.banner):
                pserv += ' ({0})'.format(serv.banner)
            print(pserv)
    print(nmap_report.summary)


def main():
    options = '-Pn -sV -p '

    try:
        report = NmapParser.parse_fromfile('masscan.xml')
    except NmapParserException as e:
        print("Scan parsing failed: {0}".format(e.msg))

    report_dict = defaultdict(list)
    for host in report.hosts:
        for service in host.services:
            report_dict[host.ipv4].append(service.port)

    for target, ports in report_dict.items():
        ports_formatted = ','.join(map(str, ports))
        print('\n')
        print('***************{0}***************'.format(target))
        print("Getting ready to scan {0} on ports {1}".format(target, ports_formatted))
        report = do_scan(target, options + ports_formatted)

        if report:
            print_scan(report)
        else:
            print('No results returned')

if __name__ == "__main__":
    main()
