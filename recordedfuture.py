import os
import re
import sys
import urllib
from datetime import datetime
from bs4 import BeautifulSoup,CData
from itertools import islice
from urllib.request import Request , urlopen , urlretrieve

def CVEFetch(strs):
    try:
        CVE=re.findall('(CVE-[0-9]*-[0-9]*)',strs)
        CVE=', '.join(list(set(CVE)))
        if not CVE:
            CVE='NA'
        return CVE
    except Exception as e:
        print('Error : ',e)


def main():
    try:
        
        proxy_support = urllib.request.ProxyHandler({'http' : 'http://672164:@proxy.cognizant.com:6050'})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_support, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        req = Request('https://www.recordedfuture.com/feed/', headers={'User-Agent': 'Mozilla/5.0'} )
        
        response= urllib.request.urlopen(req)
       
        soup=BeautifulSoup(response.read(),'html.parser') 
        items = soup.find_all('item')
        #print(items)
        for item in items:
            title=item.find_all('title')
            title=title[0].get_text()
           
            link= item.find_all('link')
            link= link[0].get_text()
            
            month = {'Jan' : '01',
                              'Feb' : '02',
                              'Mar' : '03',
                              'Apr' : '04',
                              'May' : '05',
                              'Jun' : '06',
                              'Jul' : '07',
                              'Aug' : '08',
                              'Sep' : '09',
                              'Oct' : '10',
                              'Nov' : '11',
                              'Dec' : '12',
                                  }

            pubdate= item.find_all('pubdate')
            pubdate=pubdate[0].get_text()
            pubdate=pubdate.split()
            pubdate = pubdate[3] + '-' + month[pubdate[2]] + '-' +pubdate[1] + 'T' +pubdate[4] + '.000' + '-07:00'
           
            
            desc= item.find_all('description')
            desc= desc[0].get_text()
            
            content=item.find_all('content:encoded')
            
            content=content[0].get_text()
            
            content1=BeautifulSoup(content,'html.parser')
            for div in item.find_all('a', {'rel':'nofollow'}):
                div.decompose()
           
            print('\n\nTitle : ',title,'\n\nSource : ',link,'\n\nPublished Date :',pubdate,'\n\nDescription :',content1.get_text())
    except Exception as e:
        print('Error : ',e)  
      
main()
