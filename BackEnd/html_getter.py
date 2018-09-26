#!/usr/bin/env python
import sys
import urllib2
import time
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


proxies = []
ua = UserAgent()
timeout = 0;

def main():

    global timeout;
    if timeout > 10:
        return "Error 1: Proxy Error"
    
    desc = '';
    url = "http://powerlisting.wikia.com/wiki/Special:Random";
    
    with open('/home/dtinpa/quirkregistry.com/BackEnd/proxies.txt') as f:
        line = random_line(f);

        try:
            proxy = "http://" + line.rstrip('\n');
            print(proxy);
            pageSource = scraper(url, proxy);
            desc = parser(pageSource);
            print(desc);
            return desc;
        except Exception as e:
            time.sleep(0.5);
            timeout += 1;
            print(e);
            main();
            
    return desc;


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

def scraper(url, prox):
    proxy = urllib2.ProxyHandler({'http' : prox});
    opener = urllib2.build_opener(proxy);
    urllib2.install_opener(opener);
    response = urllib2.urlopen(url);

    return response.read();

def parser(pageSource):
    soup = BeautifulSoup(pageSource, 'html.parser');
    capabilities = soup.find(id="mw-content-text");
    pTags = capabilities.find_all("p");
    descHtml = pTags[abs(len(pTags) - 1)];
    desc = descHtml.get_text();

    return desc;

if __name__ == "__main__":
    print(main());
    
