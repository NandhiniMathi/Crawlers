#Threatpost

import os
import re
import sys
import pyodbc
import urllib
import zipfile
import xlsxwriter
from bs4 import BeautifulSoup
from itertools import islice
from urllib.request import Request , urlopen , urlretrieve

new=0

def dbexporter(pid,title,link,pubdate,category,desc,reflink,fulldesc):
    global new
    cnxn=pyodbc.connect("DRIVER={SQL Server};SERVER=LT049628\SQLEXPRESS201432;DATABASE=ThreatIntel")
    cursor = cnxn.cursor()

    cursor.execute('Select count(1) as exist from news_feeds where src = \'threatpost\' and pid='+pid)
    res=cursor.fetchall()
    if(res[0].exist)==0:
        new+=1
        category=re.sub('[\'|\[|\]]','',category)         
        title=re.sub("'","`",title)
        desc=re.sub("'","`",desc)
        fulldesc=re.sub("['|’]","`",fulldesc)
        fulldesc=re.sub('"','``',fulldesc)
        cursor.execute("Insert into news_feeds(pid,title,link,pubdate,category,descr,reflink,fulldesc,src) values(\'"+pid+
                       "\',\'" + title+
                       "\',\'" + link+
                       "\',\'" + pubdate+
                       "\',\'" + category+
                       "\',\'" + desc+
                       "\',\'" + reflink+
                       "\',\'" + fulldesc+
                       "\',\'threatpost\')"
                       )
        cnxn.commit()    

def main(self,user, pwd, path):
    global new
    new=0
    path = '%s\\TI\\'%os.environ['APPDATA']
    if not os.path.exists(path):
        os.makedirs(path)
        os.makedirs(str(path)+'Tmp\\')

    entries=[]
    cveid=''
    links=[]
    info=[]
    desc=''
    pubdate=''
    moddate=''
    score='NA'
    accessvct='NA'
    accesscomplexity='NA'
    authentication='NA'
    confidentiality='NA'
    integrity='NA'
    availability='NA'
        
#---------------------------------------    
    user='577537'
    pwd='password'
#---------------------------------------
    try:
        req = Request('https://threatpost.com/feed/', headers={'User-Agent': 'Mozilla/5.0'} )
        response= urllib.request.urlopen(req)

        soup=BeautifulSoup(response.read(),'html.parser')
        items = soup.find_all('item')
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
            pubdate = pubdate[3] + '-' + month[pubdate[2]] + '-' +pubdate[1] + 'T' +pubdate[4] + '.000' + pubdate[5]
            print(pubdate)
            
            category= item.find_all('category')
            i=0
            for entry in category:
                category[i]=entry.get_text()
                i+=1

            reflink=item.find_all('guid')
            reflink=reflink[0].get_text()
            
            desc=item.find_all('description')
            desc=desc[0].get_text()
            
            pid=item.find_all('post-id')
            pid=pid[0].get_text()

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
            dbexporter(pid,title,link,pubdate,str(category),desc,reflink,full_desc)
        self.count+=1
    except:
        print('using proxy')
        proxy_support = urllib.request.ProxyHandler({'https' : 'https://'+user+':'+pwd+'@proxy.cognizant.com:6050'})
        auth = urllib.request.HTTPBasicAuthHandler()
        opener = urllib.request.build_opener(proxy_support, auth, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        try:
            req = Request('https://threatpost.com/feed/', headers={'User-Agent': 'Mozilla/5.0'} )
            response= urllib.request.urlopen(req)

            soup=BeautifulSoup(response.read(),'html.parser')
            items = soup.find_all('item')
            for item in items:
                title=item.find_all('title')
                title=title[0].get_text()
                
                link= item.find_all('link')
                link= link[0].get_text()
                
                pubdate= item.find_all('pubdate')
                pubdate=pubdate[0].get_text()
                
                category= item.find_all('category')
                i=0
                for entry in category:
                    category[i]=entry.get_text()
                    i+=1

                reflink=item.find_all('guid')
                reflink=reflink[0].get_text()
                
                desc=item.find_all('description')
                desc=desc[0].get_text()
                
                pid=item.find_all('post-id')
                pid=pid[0].get_text()

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
                dbexporter(pid,title,link,pubdate,str(category),desc,reflink,full_desc)
            self.count+=1
        except Exception as e:
            print('\nConnection error.Please check internet/proxy settings. Error : \n')
            print(e)
            self.count+=1
    print('\nNews feeds collected : ' + str(new) + '\n')

if __name__ == '__main__' :
    while True:
        print('1. Collect data feeds\n0. Exit')
        ch=input()
        if ch=='1':
            main('','','','')
        elif ch=='0':
            sys.exit(0)

