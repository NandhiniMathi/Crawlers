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
        req = Request('https://blog.comodo.com/feed/', headers={'User-Agent': 'Mozilla/5.0'} )
        response= urllib.request.urlopen(req)

        soup=BeautifulSoup(response.read(),'html.parser') 
        items = soup.find_all('item')
        
        for item in items:
            title=item.find_all('title')
            title=title[0].get_text()
            #print('Title: ',title)
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
            #pubDate=item.find_all('pubdate')
            #pubDate=pubDate[0].get_text()
            desc= item.find_all('description')
            desc= desc[0].get_text()
            
            content=item.find_all('content:encoded')
            
            content=content[0].get_text()
            content = re.sub('\[...]', '', content)
            content1=BeautifulSoup(content,'html.parser')
            
            #desc=BeautifulSoup(desc,'html.parser')
            #content=item.find_all('description')
            
            #content=content[0].get_text()
            category2 = item.find_all('category')
            
            category=[]
            for category1 in category2: 
                category.append(category1.get_text())
            
            '''
            
            
            
           
            if str(category).find('Malware','Botnet')!=-1:
                print ('open')
                    #dbexportermal(CVE,title,link,pubdate,desc,full_desc,category,src,DB)
                #dbexportermal(cve,title,link,pubDate,desc,content1.get_text(),category,'secureList',DB)
            #elif str(category).find('Vulnerabilities')!=-1:
                    #dbexporterVul(CVE,title,desc,desc,full_desc,'',category,pubdate,pubdate,link,'','',src,'','0','','','','','','',DB)
               # dbexporterVul(cve,title,desc,'',content1.get_text(),'',category,pubDate,'',link,'','','secureList','','0','','','','','','',DB)
            #else:              
                #dbexporter(cve,title,link,pubDate,desc,content1.get_text(),category,'secureList',DB)
        
            #print('###################\nTitle:',title,'\n\n',desc,'\n\n\n\nContent1::::',content1.get_text(),'\n\nSource:',link,'\n\nCategory:',category,'\n\nCVE:',cve,pubDate,'\n###################')
             '''
            print('\n\nTitle : ',title,'\n\nSource : ',link,'\n\nPublished Date :',pubdate,'\n\nDescription :',content1.get_text(),'\n\nCategory :',category)
    except Exception as e:
        print('Error : ',e)  
      
main()
