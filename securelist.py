import os
import re
import sys
import urllib
from datetime import datetime
from bs4 import BeautifulSoup,CData
from itertools import islice
from urllib.request import Request , urlopen , urlretrieve

def dbexporter(CVE,title,link,pubdate,desc,fulldesc,category,src,DB):
    try:
        cnxn=pyodbc.connect(DB)
        cursor = cnxn.cursor()
        cursor.execute('Select count(1) as exist from Nandhini_News where title =\''+title+'\'')
        res=cursor.fetchall()
        if(res[0].exist)==0:
            cursor.execute("Insert into Nandhini_News(CVE_ID,Title,Source,Reported_Date,Category,Short_Description,Description,SourceSite) values(\'" + CVE+
                           "\',\'" + title+
                           "\',\'" + link+
                           "\',\'" + pubdate+
                           "\',\'" + category+
                           "\',\'" + desc+
                           "\',\'" + fulldesc+
                           "\',\'" + src+
                           "\')"
                           )
            cnxn.commit()
            
    except Exception as e:
        print('DB ERROR!',e)
        
def CVEFetch(strs):
    try:
        CVE=re.findall('(CVE-[0-9]*-[0-9]*)',strs)
        CVE=', '.join(list(set(CVE)))
        if not CVE:
            CVE='NA'
        return CVE
    except Exception as e:
        print('Error : ',e)


def secureList(DB):
    try:
        proxy_support = urllib.request.ProxyHandler({'https' : 'https://672164:@proxy.cognizant.com:6050'})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_support, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        req = Request('https://securelist.com/feed/', headers={'User-Agent': 'Mozilla/5.0'} )
        response= urllib.request.urlopen(req)

        soup=BeautifulSoup(response.read(),'html.parser')
        items = soup.find_all('item')
        
        for item in items:
            title=item.find_all('title')
            title=title[0].get_text()
            
            link= item.find_all('link')
            link= link[0].get_text()
           
            desc=item.find_all('description')
            desc=desc[0].get_text()
            
            category2 = item.find_all('category')
            category=[]
            for category1 in category2: 
                category.append(category1.get_text())
            
            pubDate=item.find_all('pubdate')
            pubDate=pubDate[0].get_text()
            content=item.find_all('content:encoded')
            
            content=content[0].get_text()
            content1=BeautifulSoup(content,'html.parser')
            cve = CVEFetch(content1.get_text())
            print ('open')
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
             
    except Exception as e:
        print('Error : ',e)  
DB="DRIVER={SQL Server};SERVER=PC283230\MSSQL2014ENT;DATABASE=ThreatIntel_TEST"

        
secureList(DB)
