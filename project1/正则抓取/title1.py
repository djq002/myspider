比如使用lxml扩展包来解析:

from lxml import html
doc = html.parse('http://www.apple.com/')
title = doc.find('.//title').text
print title
或者使用BeautifulSoup来解析:

def  gettitle(gurl):
   doc = html.parse(gurl)
   gtitle = doc.find('.//title').text
   return gtitle
   






import urllib
from BeautifulSoup import BeautifulSoup


def gettitle2(gurl1):
   reg1 = re.compile('<[^>]*>')
   gdata = urllib.urlopen(gurl1).read()
   soup = str(BeautifulSoup(gdata).find('title'))
   soup = reg1.sub('',soup)
   return soup
   
   return soup
print soup.find('title')

#去掉网页标签
reg = re.compile('<[^>]*>') 

print(reg.sub('',html))