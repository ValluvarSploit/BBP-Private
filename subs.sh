#!/bin/bash

TARGET=$1
sudo apt-get install python3-setuptools;
wget -q -i requirements/subdomain-enum.txt; unzip amass_linux_amd64.zip; tar -xzvf subfinder_2.4.7_linux_amd64.tar.gz;
go env -w GOPATH=~/Downloads;
go get -u github.com/tomnomnom/assetfinder;
cp ~/Downloads/bin/assetfinder .; 
git clone https://github.com/m8r0wn/subscraper ; cd subscraper; sudo python3 setup.py install; cd .. ;
git clone https://github.com/aboul3la/Sublist3r.git
pip3 install -r Sublist3r/requirements.txt
python3 subscraper/subscraper.py "$TARGET" -o subdomains-auto.txt ;
python3 Sublist3r/sublist3r.py -d "$TARGET" -t 10 -v -o sublist3r.txt > /dev/null          
./amass_linux_amd64/amass enum -passive -d "$TARGET" -rf resolvers.txt > amass-passive.txt ;
./assetfinder --subs-only "$TARGET" -silent | tee -a subdomains-auto.txt;  
./subfinder -d "$TARGET" -all -o subfinder-key.txt -rL resolvers.txt ; 
./findomain -t "$TARGET" -q | tee -a subdomains-auto.txt; 

