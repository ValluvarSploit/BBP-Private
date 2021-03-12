#!/bin/bash


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
END='\033[0m'

help() {
   echo "Options:"
   printf "\t-l Subdomains file\n"
   printf "\t-o Output file (.csv)\n"
   echo ""
   echo "Example:"
   printf "\t./dnsc.sh -l subdomains.txt -o output.txt"
   exit 0
}

while getopts "l:o:" option
do
   case "$option" in
      l ) subdomains="$OPTARG" ;;
      o ) output="$OPTARG" ;;
      ? ) help ;;
   esac
done

if [ -z "$subdomains" ] || [ -z "$output" ]
then
   help
fi

printf "\n${YELLOW}[*] DNS Enumeration Started...\n${END}"

echo host,cname,status > $output

for host in $(cat $subdomains); do
dig $host > dig_result.txt 
dns_status=$(cat dig_result.txt | grep status | awk '{print $6}' | cut -d "," -f1)
dns_cname=$(cat dig_result.txt | grep CNAME | head -n1 | awk '{print $5}' | head -c -2)
printf "${YELLOW}Host:${END} $host, ${YELLOW}Status:${END} $dns_status, ${YELLOW}CNAME:${END} $dns_cname\n"
echo $host,$dns_status,$dns_cname >> $output
done

rm dig_result.txt 
