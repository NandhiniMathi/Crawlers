import os
import re
import sys
import urllib
from datetime import datetime
from bs4 import BeautifulSoup
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

def techRepublic(DB):
    try:
        proxy_support = urllib.request.ProxyHandler({'https' : 'https://672164:@proxy.cognizant.com:6050'})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_support, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        req = Request('https://www.techrepublic.com/rssfeeds/topic/security/', headers={'User-Agent': 'Mozilla/5.0'} )
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
            #desc=BeautifulSoup(desc,'html.parser')
            #desc=desc.get_text()
            #desc=desc.strip()
            #desc=re.sub('read more$','',desc)
            #desc=re.sub('\n','',desc)

            pubDate=item.find_all('pubdate')
            pubDate=pubDate[0].get_text()
            print(title)
            req = Request(link, headers={'User-Agent': 'Mozilla/5.0'} )
            response= urllib.request.urlopen(req)
            soup=BeautifulSoup(response.read(),'html.parser')
            description = soup.find_all('div', {'class':'content'})
            #print(description)
            for div in soup.find_all('div', {'class':['relatedContent pinbox pull-right','newsletter-promo','ad-inpage-video-top','sharethrough-article','ad-sharethrough-top']}):
                div.decompose()
            for div in soup.find_all('figure', {'class':'image pull-none image-large'}):
                div.decompose()
            for div in soup.find_all('a'):
                div.decompose()
            
            try:
                print(description[0].get_text().strip())
            except:
                pass
             #t2=soup.find_all('div',{'class':'container-button-unsub'})
             #t2.decompose()'''
    except Exception as e:
        print('Error : ',e)


   
DB="DRIVER={SQL Server};SERVER=PC283230\MSSQL2014ENT;DATABASE=ThreatIntel_TEST"

techRepublic(DB)
