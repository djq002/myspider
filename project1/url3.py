#coding=utf8
import  urllib2
import  sgmllib 
import  MySQLdb

class LinksParser(sgmllib.SGMLParser):  
 urls = []  
 def do_a(self, attrs):  
  for name, value in attrs:  
   if name == 'href' and value not in self.urls:    #防止重复采集
    if value.startswith('http'):  
      self.urls.append(value)  
 #     print value  
    else:  
     continue  
    return  

wurl = raw_input('input the url:')  
p =  LinksParser()  
f = urllib2.urlopen(wurl)  


p.feed(f.read())  

#---------- input into the database
try:
   db = MySQLdb.connect('localhost','root','djq002','python')
   cur = db.cursor()
   print 'succeed in connect!!'
except:
   print 'connect error!!'


m = 1
for url in p.urls:  
   sql = 'insert into url(url) select'+' '+'\"'+url+'\"'
   #cur.execute(sql)
   cur.execute(sql)

   db.commit()
   
   print 'The'+str(m)+':'+url
   m=m+1
   
print
print
print 'done!!'
print
db.close()
f.close()  
p.close()  

