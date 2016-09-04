#coding=utf8
import urllib2
import MySQLdb
import sys
import socket
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
   


clinks = mysqlexe('select url from url','python')
mysqlexe('truncate url','python')
print '数据表已清空！！'
c1 = 0
c2 = 0
print 'checking start!!'
for cline1 in clinks:
   c1 =c1+1
   try:
       op = urllib2.urlopen(cline1[0])
       gcode = op.getcode()
       if gcode==200:
           csql1 = 'insert into url(url) select '+'\''+cline1[0]+'\''
           mysqlexe(csql1,'python')
           c2 = c2+1
           print cline1[0],'       [ available!!]'
   except:
       csql2 = 'insert into dead(url) select '+'\''+cline1[0]+'\''   
       mysqlexe(csql2,'python')
       print cline1[0],'           [death!!]'
print '检查链接数为：',c1,'可用链接数为：',c2	   
	   



      


