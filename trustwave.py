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
        proxy_support = urllib.request.ProxyHandler({'https' : 'https://672164:@proxy.cognizant.com:6050'})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_support, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        req = Request('https://www.trustwave.com/rss.aspx?type=slblog', headers={'User-Agent': 'Mozilla/5.0'}) 
        res = urllib.request.urlopen(req)
        soup=BeautifulSoup(res.read(),'html.parser')
        
        items = soup.find_all('item')
        
        for item in items:
            title=item.find_all('title')
            title=title[0].get_text()
            print(title,'\n\n')
            link= item.find_all('link')
            link= link[0].get_text()
            print(link,'\n\n')
            desc=item.find_all('description')
            desc=desc[0].get_text()
            #desc = re.sub('\[...]', '', desc)
            desc=BeautifulSoup(desc,'html.parser')
            #print(soup1.get_text())
            
            print(desc.get_text(),'\n\n')
            full_desc=''
            try:
                req = Request(link, headers={'User-Agent': 'Mozilla/5.0'} )
                response= urllib.request.urlopen(req)
                soup=BeautifulSoup(response.read(),'html.parser')
                containers=soup.find_all('div')
                for container in containers:
                    try:
                        if str(container['class'][0])=='entry-content' :
                            texts=container.find_all('p')
                            for text in texts:
                                text=text.get_text()
                                full_desc+=text
                    except:
                        pass
            except:
                pass
            print(full_desc,'\n\n')
            
            #pubDate=item.find_all('pubdate')
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
            #pubDate=pubDate[0].get_text()
            print(pubdate,'\n\n')
            '''
            category2 = item.find_all('category')
            category=[]
            for category1 in category2: 
                category.append(category1.get_text())

            print(category,'\n')
            '''
            print('***********\n\n')
    except Exception as e:
        print('Error : ',e)  
      
main()
