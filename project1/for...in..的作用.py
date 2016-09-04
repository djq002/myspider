#coding=utf8
import re
import MySQLdb
import urllib2
import HTMLParser

#-----------------------------------------------------------------------
#------------------------定义mysql数据库操作函数-----------------------
#-----------------------------------------------------------------------
def  mysqlexe(sql):
   db = MySQLdb.connect('localhost','root','djq002','python')
   cur = db.cursor()
   cur.execute(sql)
   result = cur.fetchall()
   db.commit()
   return result


print  

print
content = [] 
result = mysqlexe('select url from url')
for line in result:
   
   print line[0]
   content.append(line[0])


   
url = raw_input('input the url:')
if url  in content:
   print 'mysql have a record the same as:',url


else:
   print 'nothing has the same !!'

print 
#print content 
print 'done!!'

