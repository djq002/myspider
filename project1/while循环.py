#coding=utf8
"""
from tansuozhe:djq002
"""
import urllib2
import HTMLParser
from BeautifulSoup import BeautifulSoup
from lxml import html
import MySQLdb
import re
import sys
import socket
socket.setdefaulttimeout(10.0)
reload(sys)
sys.setdefaultencoding("utf-8")     # 重新加载系统并设置默认编码



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
   

#------------------------------------------------------------------------------
#--------------------- 定义一个用于获取网页title的函数 step2------------------
#------------------------------------------------------------------------------
def gettitle(gurl): 
   gtitle = '招聘信息'
   try:
       doc = html.parse(gurl)
       gtitle = doc.find('.//title').text
       return gtitle
   except:
       return gtitle

def gettitle2(gurl1):
   soup = '招聘信息'
   try :
      reg1 = re.compile('<[^>]*>')
      gdata = urllib2.urlopen(gurl1).read()
      soup = str(BeautifulSoup(gdata).find('title'))
      soup = reg1.sub('',soup)
      return soup
   except:
       return soup
   
   
   
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


        



#if __name__ == '__main__':

#----------------------------------------------------------------------------
#--------------------------- 获取种子 step4---------------------------------
#----------------------------------------------------------------------------
lo = 'y'
my = MParser()
collection = []
while lo == 'y':
# 获取url并打开url进行数据读取
   print 
   print
   url = raw_input('输入导航网址：')
   op1 = urllib2.urlopen(url)
   fdata1 = op1.read()
   op1.close()
   my.feed(fdata1)

   print 
   print 'collecting !!'
   print
   
   try:
       for surl in  my.mvalue:
	        if surl not in collection:	        
                  collection.append(surl)
                   print '捕获到url：',surl
               
       print 
       print 'done !!' 
       print '*****************************'
       lo = raw_input('want to again?(y/n):')
       
       my.mvalue = []
       print
        
   except HTMLParser.HTMLParseError,e:
       pass

   
#----------------------------------------------------------------------------
#--------------------------- 搜索目标url step5------------------------------
#----------------------------------------------------------------------------
print 'url捕获结束!!'
print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
print 'The Next:'
print 
print '          Hunting start !!!'



m1 = 0
myp = MParser()
while m1 <len(collection):
   myp.mvalue = []
   try:     
       op2 = urllib2.urlopen(collection[m1])
       fdata2 = op2.read()
       op2.close()       
       myp.feed(fdata2)
   except :	
       continue  
   for joburl in myp.mvalue:
       judge1 = re.match(r'.*(/hr\.|\.hr|/hr/|Hr|career|Career|job|Job|jobs|/join/|Join|join\.|joinus|Joinus|recruit|Recruit|zhaopin|ZhaoPin|zpxx|ZPXX|rczp|RCZP|zpyc|ZPYC|zp|ZP|zxnc|ZXNC|yrln|YRLN|rcjh|RCJH|zhaoxiannaishi|employer|Employer|campus|Campus){1}.*',joburl)
	   result3 = mysqlexe('select url from joburl')
       content3 = []
       for line2 in result3:
           content3.append(line2[0])   
       if judge1 != None and joburl not in content3:           
           mytitle = gettitle2(joburl)          
           print 'collect: <',mytitle,joburl,'>'
           sql3 = 'insert into joburl(url,title) select'+' '+'\"'+str(joburl)+'\"'+','+'\"'+str(mytitle)+'\"'
           try:
               mysqlexe(sql3)
           except:
               continue
   
            	   
print
print 
print 'hunting over!!'		   
print '***********************************************************************'
print '------------------------ tansuozhe:002 -----------------------------'
print '***********************************************************************'
print
print
		   
	   

	   
	   
	   
      

	   
