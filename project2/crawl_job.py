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
import string
#socket.setdefaulttimeout(10.0)
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


lo2 = 'no' # 控制循环

# 表名列表
table_list1 = ['','link_bank','link_car','link_computer','link_goods','link_video','link_shequ','link_money','link_hotel_gd']
table_list2 = ['','job_bank','job_car','job_computer','job_goods','job_video','job_shequ','job_money','job_hotel_gd']


while  lo2 !='exit':

# 选取抓取源
   print '抓取源：',table_list1
   print '从1到'+str(len(table_list1)-1)+'之间选取抓取源'
   source1 = string.atoi(raw_input('请选择抓取源（列表元素编号）：'))
   
   j1 = 'n'
   while j1 != 'y':
       print '你选择了',table_list1[source1],'表里的链接作为抓取源'
       j1 = raw_input('确定要选择此表？(y/n)')
       if j1 == 'n':
           source1 = string.atoi(raw_input('请重新选择抓取源（列表元素编号）：')) 
 
# 导处抓取源 
   sql1 = 'select url from '+str(table_list1[source1])
   cr_source = mysqlexe(sql1)

# 把招聘页链接加载到列表以待检查是否有重复   
   sql2 = 'select url from '+str(table_list2[source1])
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
               judge1 = re.match(r'.*(/hr\.|\.hr|/hr/|/Hr/|\.Hr|career|Career|job|Job|jobs|/join/|Join|join\.|joinus|Joinus|recruit|Recruit|zhaopin|ZhaoPin|zpxx|ZPXX|rczp|RCZP|zpyc|ZPYC|/zp/|/ZP/|zxnc|ZXNC|yrln|YRLN|rcjh|RCJH|zhaoxiannaishi|employer|Employer|campus|Campus){1}.*',joburl)
               judge2 = re.match(r'http://.*',joburl)
               if judge2 !=None:
                   if judge1 !=None:
	              
                       if joburl not in content3:           
                           mytitle = gettitle3(joburl)          
                           print 'collect: <',mytitle,joburl,'>'
                           sql3 = 'insert into '+table_list2[source1]+'(url,title)'+' select'+' '+'\"'+str(joburl)+'\"'+','+'\"'+str(mytitle)+'\"'
		   
                           try:
                               mysqlexe(sql3) 
			       content3.append(joburl)
                           except:
                               continue



  
  
   print 
   print 'done!!'
   print 
   lo2 = raw_input('press any key to continue or type\'exit\' to quit:')

   
   
   
print 
print  'process over!!' 
print   
