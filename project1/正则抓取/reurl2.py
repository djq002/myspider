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
import requests
import socket
#socket.setdefaulttimeout(10.0)
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
      
      mop = urllib2.urlopen(gurl1)
      gdata = mop.read()
      mop.close()
      soup = str(BeautifulSoup(gdata).find('title'))
      reg1 = re.compile('<[^>]*>')
      soup = reg1.sub('',soup)
      return soup
   except:
       return soup
   
# 获取title函数 V3版本
def gettile3(gurl2):   
   thetitle = '招聘信息'
   try:
       
       mop1 = urllib2.urlopen(gurl2)
       gdata1 = mop1.read()
       mop1.close()
       thetitle = str(BeautifulSoup(gdata1).find('title'))
       reg2 = re.compile('<[^>]*>')
       thetitle = reg2.sub('',thetitle) # 去掉网页标签
       return thetitle
   except:
       try:
           doc1 = html.parse(gurl2)
           thetitle = doc1.find('.//title').text
           return thetitle
       except:
           return thetitle
       
 # 获取title函数 V4版本
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
      
   
#------------------------------------------------------------------------------
#---------------------- 创建从网页上获url的类 step3 --------------------------
#------------------------------------------------------------------------------

# 模块抓取url
class MParser(HTMLParser.HTMLParser):
    mvalue = [] 
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
               if name == 'href' and value.startswith('http')and value not in self.mvalue:   			        # 检查url是否以‘http’开头以及列表mvalue是否有重复的url
                       exclude = re.match(r".*(baidu|BAIDU|BaiDu|google|GOOGLE).*",value) 					# 去除有关百度的url
		       if exclude ==None:
                           self.mvalue.append(value)

# 正则抓取url 
def geturl(surl):
   r = requests.get(surl)
   data = r.text 
   link_list =re.findall(r"(?<=href=\")[http://]{1}.+?(?=\")|(?<=href=\')[http://]{1}.+?(?=\')" ,data)
   return link_list
        





#----------------------------------------------------------------------------
#--------------------------- 获取种子 step4---------------------------------
#----------------------------------------------------------------------------


theloop = 'lo' # 外层循环
lo = 'y'       # 内层循环
my = MParser() 

while theloop !='eixt':
   mysqlexe('truncate surl')
   while lo != 'n':
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
# 获取mysql url 表里的所有记录，并加载到列表里面
               content1 = [] 
               result1 = mysqlexe('select url from url')
               for line in result1:      
                   content1.append(line[0])

	       if surl not in content1:	        
                   sql2 =  'insert into url(url) select'+' '+'\"'+surl+'\"'
                   sql2_1 =  'insert into surl(url) select'+' '+'\"'+surl+'\"'
	           mysqlexe(sql2)
                   mysqlexe(sql2_1)
                   
                   print '捕获到url：',surl
               
           print 
           print 'done !!' 
           print '*****************************'
           lo = raw_input('want to scrapy again?(y/n):')
       
           my.mvalue = []
           print
        
       except :
           pass
   
   
#----------------------------------------------------------------------------
#--------------------------- 搜索目标url step5------------------------------
#----------------------------------------------------------------------------
   print 'url捕获结束!!'
   mylist = ['\'http://www.zhaopin.com%\'','\'%58.com/%\'','\'%ganji.com/%\'','\'http://www.liepin.com%\'','\'http://www.chinahr.com%\'','\'http://www.jobcn.com%\'','\'http://www.lagou.com%\'','\'http://www.51job.com%\'','\'www.chinahr.com\'']
   del1 = 'delete from surl where url like '
   for line4 in mylist:
       del_sql = del1+line4
       mysqlexe(del_sql)
   print 'clear done!!'

   print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
   print 'The Next:'
   print '[>>>>>>>>>>>[Hunting start !!!]<<<<<<<<<<<<<]'
   print
   print
   qdata = mysqlexe('select url from surl') 
   for seed1  in qdata: 
       try:
           myvalue = geturl(seed1[0]) 
             
       except :	
           continue      
	   	   	  	   
   
       for joburl in myvalue:
           judge1 = re.match(r'.*(/hr\.|\.hr|/hr/|/Hr/|\.Hr|career|Career|job|Job|jobs|/join/|Join|join\.|joinus|Joinus|recruit|Recruit|zhaopin|ZhaoPin|zpxx|ZPXX|rczp|RCZP|zpyc|ZPYC|/zp/|/ZP/|zxnc|ZXNC|yrln|YRLN|rcjh|RCJH|zhaoxiannaishi|employer|Employer|campus|Campus){1}.*',joburl)
           judge2 = re.match(r'http://.*',joburl)
           if judge2 !=None:
               if judge1 !=None:
	           result3 = mysqlexe('select url from joburl')
                   content3 = []
                   for line2 in result3:
                       content3.append(line2[0])   
                   if joburl not in content3:           
                       mytitle = gettitle2(joburl)          
                       print 'collect: <',mytitle,joburl,'>'
                       sql3 = 'insert into joburl(url,title) select'+' '+'\"'+str(joburl)+'\"'+','+'\"'+str(mytitle)+'\"'
                       try:
                           mysqlexe(sql3)
                       except:
                           continue
   theloop = raw_input('press any key to continue:(type \'eixt\'to kill the process):')
   if theloop != 'exit' or theloop != 'quit':
       lo = 'y'
   
mysqlexe("update joburl set title=\'诚聘英才\' where title=\'\' ")
mysqlexe("update joburl set title=\'诚聘英才\' where title=\'none\' ")
print
print 
print '>>>>>>>>>>>>>>[hunting over!!]<<<<<<<<<<<<<<<'		   
print
print
print '***********************************************************************'
print '------------------------ From 第四小组 -----------------------------'
print '***********************************************************************'
print
print
		   
	   

	   
	   
	   
      

	   
