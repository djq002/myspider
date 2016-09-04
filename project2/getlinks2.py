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
from multiprocessing.dummy import Pool

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
   

   
#------------------------------------------------------------------------------
#---------------------- 创建从网页上获url的类 step3 --------------------------------
#------------------------------------------------------------------------------
class MParser(HTMLParser.HTMLParser):
    mvalue = [] 
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
               if name == 'href' and value.startswith('http') and value not in self.mvalue:   			        # 检查url是否以‘http’开头以及列表mvalue是否有重复的url
                       exclude = re.match(r".*(baidu|BAIDU|BaiDu|google|GOOGLE|www.lxs123.com|360.cn|hotelsoso.com).*",value) 					# 去除有关百度的url
		       if exclude ==None:
                           self.mvalue.append(value)


def clink(curl):
   avaurl = ''
   try:
       op = urllib2.urlopen(curl)
       code = op.getcode()
       if code==200:
          avaurl = curl
          return avaurl        
   except:     
       pass

   




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++  构造字典  ++++++++++++++++++++++++++++++++++++++++++++++
table_list = {}

# 将sql查询结果加载到字典上
m = 1
print '数据库有以下数据表可供选择：'
print 
print '键名'+'   '+'表'
tbl = mysqlexe('show tables')
exclude_list = ['link_tmp','link_exclude']
for line1 in tbl:
    # 符合条件的才加载 
   match1 = re.match(r'link{1}.*',line1[0])

   if match1!=None:
       if line1[0] not in exclude_list:
           key =str(m)   
           table_list[key] = line1[0]
           print m,':',table_list[key]
           m = m+1

   

select_table = ''
judge = ''
while judge!='y':
   mkey = str(raw_input('输入键名:'))
   while  table_list.has_key(mkey)!=True:
       mkey = str(raw_input('键名不存在，请重新输入:'))
   select_table  = table_list[mkey]
   print '你选择的表格是:',table_list[mkey]
   
   judge = raw_input('你确定要选择?(y/n):')

   
   
   
   
   
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
#++++++++++++++++++++++++++++++++++++++++++ 开始收集url +++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  
lo1 = 'continue'	
myparser =MParser()	
content1 = []
checkurls = []
		   
while 	lo1 !='exit':
   url = raw_input('输入导航网址：')
   op1 = urllib2.urlopen(url)
   fdata1 = op1.read()
   op1.close()
   myparser.feed(fdata1)

	
# 查询收集记忆库   
   sql1 = 'select url from collect_memory'
   col_memory = mysqlexe(sql1)
   for line2 in col_memory:
      content1.append(line2[0])  
# 去重复	  
   for surl in myparser.mvalue:
       if surl not in content1:
	       checkurls.append(surl)
               content1.append(surl)

# 执行检查——去死链接
   print 'checking!! please wait...'
   mpool = Pool(8)	   
   result = mpool.map(clink,checkurls)
   mpool.close()
   mpool.join()
   
   for line3 in result:       	   
       if line3!=None:
	       try:
	           sql2 = 'insert into '+select_table+'(url) '+' select ' +' \''+str(line3)+'\''
	           sql3 = 'insert into collect_memory(url) select '+' \''+str(line3)+'\''
	           mysqlexe(sql2)
	           mysqlexe(sql3)
                   print 'collect:'+line3
	                
	       except:
                   pass	 	   
# 清空列表		   
   content1 = []		   
   myparser.mvalue = []
   checklinks = []
   lo1 = raw_input('press any to continue or\'exit\' to quit:')	   
   
print   					   
print
print 'process over!!'

