#coding=utf8
import urllib2
import MySQLdb
import sys
import socket
import thread
from multiprocessing.dummy import Pool
import time
#socket.setdefaulttimeout(10.0)
reload(sys)
sys.setdefaultencoding("utf-8") 


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++ 操作数据库的函数 +++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def mysqlexe(sql,db):
   conn = MySQLdb.connect('localhost','root','djq002',db,charset='utf8')
   cur = conn.cursor()
   cur.execute(sql)
   result = cur.fetchall()
   conn.commit()
   conn.close()
   return result
   
def clink(curl):
   try:
       op = urllib2.urlopen(curl)
       code = op.getcode()
       if code==200:
           print 'From:',':',curl,'      [available]'
       else:
           print 'From:',':',curl,'      [unavailable]'
   except:
       print 'From:',':',curl,'    [unavailable]'



clinks = mysqlexe('select url from url','python')
checkurls = []
for cline in clinks:
   checkurls.append(cline[0])

mypool = Pool(4)
t1 = time.time()
result = mypool.map(clink,checkurls)
mypool.close()
mypool.join()
t2 = time.time()
print 'cost:',t2-t1





