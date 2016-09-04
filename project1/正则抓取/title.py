#coding=utf8
import urllib2
import MySQLdb
from lxml import html
from BeautifulSoup import BeautifulSoup
import socket
import HTMLParser
import requests
import re
socket.setdefaulttimeout(5.0)





# 获取网页内容 
def geturl(surl):
   r = requests.get(surl)
   data = r.text
   # 利用正则查找所有连接
  
   link_list =re.findall(r"(?<=href=\")[http://]{1}.+?(?=\")|(?<=href=\')[http://]{1}.+?(?=\')" ,data)
   return link_list



#------------------------------------------------------------------------------
#---------------------------- 定义操作mysql函数 step1-------------------------
#------------------------------------------------------------------------------
def  mysqlexe(sql):
   db = MySQLdb.connect('localhost','root','djq002','python',charset='utf8')
   cur = db.cursor()
   cur.execute(sql)
   result = cur.fetchall()
   db.commit()
   db.close()
   return result

   
   
   
#-----------------------------------------------------------------------------   
#----------------------- 定义获取网页标题的函数  ----------------------------
#-----------------------------------------------------------------------------


# 获取title函数 V1版本
def gettitle(gurl): 
   gtitle = '招聘信息'
   try:
       doc = html.parse(gurl)
       gtitle = doc.find('.//title').text
       return gtitle
   except:
       return gtitle
# 获取title函数 V2版本
def gettitle2(gurl1):
   soup = '招聘信息'
   try :
      reg1 = re.compile('<[^>]*>')
	  mop = urllib2.urlopen(gurl1)
      gdata = mop.read()
	  mop.close()
      soup = str(BeautifulSoup(gdata).find('title'))
      soup = reg1.sub('',soup)
      return soup
   except:
       return soup



# 获取title函数 V3版本
def gettitle1(gurl1):
   soup1 = '招聘信息'
   try:
       doc1 = html.parse(gurl1)
       soup1 = doc1.find('.//title').text
       return soup1
   except:
       try :
           reg2 = re.compile('<[^>]*>')
		   mop = urllib2.urlopen(gurl1)
           gdata1 = mop.read()
		   mop.close()
           soup1 = str(BeautifulSoup(gdata1).find('title'))
           soup1 = reg2.sub('',soup1)
           return soup1
       except:
           return soup1




# 获取title函数 V4版本
def gettile3(gurl2):   
   thetitle = '招聘信息'
   try:
       reg2 = re.compile('<[^>]*>')
	   mop1 = urllib2.urlopen(gurl2)
       gdata1 = mop1.read()
	   mop1.close()
       thetitle = str(BeautifulSoup(gdata1).find('title'))
       thetitle = reg2.sub('',thetitle)
       return thetitle
   except:
       try:
           doc1 = html.parse(gurl2)
           thetitle = doc1.find('.//title').text
           return thetitle
       except:
           return thetitle


   
#------------------------------------------------------------------------------
#---------------------- 创建从网页上获url的类 step3 --------------------------------
#------------------------------------------------------------------------------
class MParser(HTMLParser.HTMLParser):
    mvalue = [] 
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
               if name == 'href' and value.startswith('http'):
#and value not in self.mvalue:   			        # 检查url是否以‘http’开头以及列表mvalue是否有重复的url
                       exclude = re.match(r".*(?=baidu|BAIDU|BaiDu).*",value) 					# 去除有关百度的url
		       if exclude ==None:
                           self.mvalue.append(value)


#list1 = ['http://www.google.com','http://www.baidu.com','http://www.mi.com','http://www.4399.com','http://www.huxiu.com']
#sql = 'select url from url'
#list1 = mysqlexe(sql)
#myp = MParser()
url1 = raw_input('input the url:')
url_list = geturl(url1)

for url in url_list:
   try :
       op = urllib2.urlopen(url)
       fdata = op.read()
       op.close()
       
       print ':', gettitle2(url)
   except:
       pass
  #     print '404:',url[0]



