#!/bin/bash

TARGET=$1
sudo apt-get install python3-setuptools;
wget -q -i requirements/subdomain-enum.txt; mv findomain-linux findomain; unzip amass_linux_amd64.zip; tar -xzvf subfinder_2.4.7_linux_amd64.tar.gz;
go env -w GOPATH=~/Downloads;
go get -u github.com/tomnomnom/assetfinder;
cp ~/Downloads/bin/assetfinder .; 
git clone https://github.com/m8r0wn/subscraper ; cd subscraper; sudo python3 setup.py install; cd .. ;
git clone https://github.com/aboul3la/Sublist3r.git
pip3 install -r Sublist3r/requirements.txt

echo 'Subscraper Enumeration'
python3 subscraper/subscraper.py "$TARGET" -o subscraper.txt;

echo 'Sublist3r Enumeration'
python3 Sublist3r/sublist3r.py -d "$TARGET" -t 10 -v -o sublist3r.txt > /dev/null          

echo 'Amass Enumeration'
./amass_linux_amd64/amass enum -passive -d "$TARGET" -rf resolvers.txt -o amass-passive.txt ;

echo 'Assetfinder Enumeration'
./assetfinder --subs-only "$TARGET" -silent | tee assetfinder.txt;  

echo 'Subfinder Enumeration'
./subfinder -d "$TARGET" -all -o subfinder-key.txt -rL resolvers.txt ; 

echo 'Findomain Enumeration'
./findomain -t "$TARGET" -q | tee findomain.txt; 

cat subscraper.txt sublist3r.txt amass-passive.txt assetfinder.txt subfinder-key.txt findomain.txt >> recursive-subdomains.txt
sort -u recursive-subdomains.txt -o recursive-subdomains.txt
