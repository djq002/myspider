#coding=utf8
"""
from tansuozhe:djq002   全自动版
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
import string
socket.setdefaulttimeout(8.0)
reload(sys)
sys.setdefaultencoding("utf-8")     # 重新加载系统并设置默认编码




#------------------------------------------------------------------------------
#---------------------------- 定义操作mysql函数 step1-------------------------
#------------------------------------------------------------------------------
def  mysqlexe(sql):
   db = MySQLdb.connect('localhost','root','djq002','joblinks',charset='utf8')
   cur = db.cursor()
   cur.execute(sql)
   result = cur.fetchall()
   db.commit()
   db.close()
   return result
   
   
   
   
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
		   
		   
# 获取title函数 V4版本
def gettitle3(gurl2):   
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
		   
		   
		   
		   
# 正则抓取url 
def geturl(surl):
   r = requests.get(surl)
   data = r.text 
   link_list =re.findall(r"(?<=href=\")[http://]{1}.+?(?=\")|(?<=href=\')[http://]{1}.+?(?=\')" ,data)
   return link_list
   

   





#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++ 抓取程序 +++++++++++++++++++++++++++++++++++++++++++   
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

lo2 = 'no' # 控制循环 
while  lo2 !='exit':
   #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   #++++++++++++++++++++++++++++++++++++++++++++++++++++  构造字典  ++++++++++++++++++++++++++++++++++++++++++++++
   table_list = {}
   table_list2 = {}

   # 将sql查询结果加载到字典上
   m = 0
   m2 = 0
   print '数据库有以下数据表可提供抓取源：'
   print 
   print '键名'+'  | '+'表'
   tbl = mysqlexe('show tables')
   exclude_list = ['link_tmp','link_exclude'] # 排除的数据表
   for mline1 in tbl:
     # 符合条件的才加载 
       match1 = re.match(r'link{1}.*',mline1[0])
       match2 = re.match(r'job{1}.*',mline1[0])
       if match1!=None:
           if mline1[0] not in exclude_list:
               key =str(m)   
               table_list[key] = mline1[0]
               print m,':',table_list[key]
               m = m+1
       if match2!=None:
	   key2 = str(m2)
	   table_list2[key2] = mline1[0]
	   m2 = m2+1
   
# 选择抓取源
   for crawlloop in range(len(table_list)):
       crawlloop = str(crawlloop)
       select_table1 = table_list[crawlloop]
       select_table2 = table_list2[crawlloop]
       print '[正在对数据表：]',table_list[crawlloop],'里的链接进行打开搜索目标链接...'
   



   # 导处抓取源 
       sql1 = 'select url from '+select_table1
       cr_source = mysqlexe(sql1)
   
   # 把招聘页链接加载到列表以待检查是否有重复   
       sql2 = 'select url from '+select_table2 
       result3 = mysqlexe(sql2)
       content3 = []
       for line2 in result3:
           content3.append(line2[0])
	   
   # 把招聘也抓取记忆表加载到列表上以待检查是否有重复
       sql5 = 'select url from crawl_memory '	   
       result4 = mysqlexe(sql5)
       content4 = []
       for line3 in result4:
           content4.append(line3[0])
   
   # 逐一打开并查找招聘页   
       for line1 in cr_source:
           if line1[0] not in content4:
	       content4.append(line1[0])
	       sql6 = 'insert into crawl_memory(url) select '+'\''+line1[0]+'\''
	       mysqlexe(sql6)
	       try:
	           job_list1 = geturl(line1[0])
               except:
                   continue	   
		   
               for joburl in job_list1:
                   judge1 = re.match(r'http(s)?://.*(hrsection|/hr\.|\.hr|/hr/|/Hr/|\.Hr|/hr|career|Career|job|Job|jobs|JobList|/join/|Join|joinus|Joinus|joinUs|recruit|Recruit|zhaopin|ZhaoPin|zpxx|ZPXX|rczp|RCZP|zpyc|ZPYC|/zp/|/ZP/|zxnc|ZXNC|yrln|YRLN|rcjh|RCJH|zhaoxiannaishi|rencaijihua|employer|Employer|employinfo|campus|Campus|Talent|talen|rcsc|retain|rcqp|zpgg|zp_list){1,}(\.|.)*',joburl)
                   judge2 = re.match(r'/{0,1}(\w*/)*(hrsection|hr|Hr|career|Career|job|Job|JobList|joinus|Joinus|join|Join|recruit|Recruit|zhaopin|ZhaoPin|zpxx|ZPXX|rczp|RCZP|zpyc|ZPYC|zp|ZP|zxnc|ZXNC|yrln|YRLN|rcjh|RCJH|zhaoxiannaishi|rencaijihua|employer|Employer|employinfo|campus|Campus|Talent|talen|rcsc|retain|rcqp|zpgg|zp_list){1,}.*',joburl)
                   if judge1 !=None or judge2!=None:	              
                       if joburl not in content3:   
                               if judge2!=None:
                                   joburl = line1[0]+joburl
                               mytitle = gettitle3(joburl)          
                               print 'collect: <',mytitle,joburl,'>'
                               sql3 = 'insert into '+select_table2+'(url,title)'+' select'+' '+'\"'+str(joburl)+'\"'+','+'\"'+str(mytitle)+'\"'
		   
                               try:
                                   mysqlexe(sql3) 
			           content3.append(joburl)
                               except:
                                   continue
       print '抓取源',table_list[crawlloop],'以搜索完毕！！'
       print '......'
       print '...'


  
  
   print 
   print 'done!!'
   print 
   lo2 = raw_input('press any key to continue or type\'exit\' to quit:')

   
   
   
print 
print  'process over!!' 
print   
   
   
   
   
   
   
