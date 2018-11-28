import os
import re
import sys
import urllib
#import pyodbc
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


def trendmicro(DB):
    try:
        proxy_support = urllib.request.ProxyHandler({'https' : 'https://672164:@proxy.cognizant.com:6050'})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_support, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
    
        req = Request('https://blog.trendmicro.com/', headers={'User-Agent': 'Mozilla/5.0'} )
        response= urllib.request.urlopen(req)
        #print()
        
        soup=BeautifulSoup(response.read(),'html.parser')
        #print(soup)
        category=[]  
        for item in soup.find_all(attrs={'class': 'post-title'}):
            for link in item.find_all('a'):
                req = Request(link.get('href'), headers={'User-Agent': 'Mozilla/5.0'} )
                page_inner= urllib.request.urlopen(req)
                title=item.find_all('h1')
                soup = BeautifulSoup(page_inner.read(), 'html.parser')
                pubdate = soup.find(attrs={'class': 'post-date'})
                pubdate = pubdate.find('a')
         
                for pubdate1 in soup.find_all(attrs={'class': 'post-cat'}):
                    for a1 in pubdate1.find_all('a'):
                        for category1 in a1: 
                            category.append(category1)
                #print('\nCategory: ',category)
                
                t=soup.find('div',{'class':'post-text'})
                for div in soup.find_all('p', {'style':'text-align: center'}):
                    div.decompose()
                for div in soup.find_all('div', {'class':'yarpp-related'}):
                    div.decompose()
                if str(category).find('Malware')!=-1:
                    #dbexportermal(CVE,title,link,pubdate,desc,full_desc,category,src,DB)
                    dbexportermal('',title[0].get_text(),link.get('href'),pubdate,'',t.get_text(),category,'trendmicro',DB)
                elif str(category).find('Vulnerabilities')!=-1:
                    #dbexporterVul(CVE,title,desc,desc,full_desc,'',category,pubdate,pubdate,link,'','',src,'','0','','','','','','',DB)
                    dbexporterVul('',title[0].get_text(),'','',t.get_text(),'',category,pubdate,'',link.get('href'),'','','trendmicro','','0','','','','','','',DB)
                else:              
                    dbexporter('',title[0].get_text(),link.get('href'),pubdate,'',t.get_text(),category,'trendmicro',DB)
                #print('\nTitle:',title[0].get_text(),'\n\n','\n\nSource:',link.get('href'),'Description:',t.get_text(),'\n\n''\n\nPubDate:',pubdate,'\nCategory: ',category,'\n###################')
    except Exception as e:
        print('Error : ',e)  
DB="DRIVER={SQL Server};SERVER=PC283230\MSSQL2014ENT;DATABASE=ThreatIntel_TEST"

trendmicro(DB)
