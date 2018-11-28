import urllib.request
from bs4 import BeautifulSoup
import base64
import re
from urllib.request import Request , urlopen , urlretrieve

global my_list
def Hackernews(urllink,mewstype):
    proxy_support = urllib.request.ProxyHandler({'https' : 'https://672164:@proxy.cognizant.com:6050'})
    auth = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_support, auth, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    req = Request(urllink, headers={'User-Agent': 'Mozilla/5.0'} )
    page= urllib.request.urlopen(req)
    #page = urllib.request.urlopen(urllink)
    soup = BeautifulSoup(page.read(), 'html.parser') 
    for item in soup.find_all(attrs={'class': 'post-title url'}):
        for link in item.find_all('a'):
            if(mewstype=='malware'):
                my_list.append(link.get('href'))
            else:
                if(link.get('href') in my_list):
                    break;
            print('Source: ',link.get('href'))
            req = Request(link.get('href'), headers={'User-Agent': 'Mozilla/5.0'} )
            page_inner= urllib.request.urlopen(req)
            #page_inner = urllib.request.urlopen(link.get('href'))
            soup = BeautifulSoup(page_inner.read(), 'html.parser')
            list = soup.findAll('article', attrs={'class':'post item module'})
            print(list)
            title = soup.find(attrs={'class': 'url entry-title page-link'})
            print('Title: ',title.text)
            Pubdate = soup.find(attrs={'itemprop': 'datePublished'})
            Author = soup.find(attrs={'class': 'author vcard byline'})
            if(Author.text.strip() =='Exclusive Deals'):
                break
            print('Published: ',Pubdate.attrs['content'])
            Update = soup.find(attrs={'itemprop': 'dateModified'})
            print('Updated: ',Update.attrs['content'])
            Desc = soup.find(attrs={'class': 'articlebodyonly'})
            Desc=(Desc.get_text())
            description=re.sub('\n','',Desc.replace('(adsbygoogle = window.adsbygoogle || []).push({});',''))
            #print(description)
    print("################")
my_list = list()
#Hackernews('http://thehackernews.com/search/label/Malware','malware')
Hackernews('https://thehackernews.com/','news')

