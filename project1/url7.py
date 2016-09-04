#coding=utf8
"""
from tansuozhe:djq002
"""
import urllib2
import HTMLParser
import MySQLdb
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")     # 重新加载系统并设置默认编码



#------------------------------------------------------------------------------
#---------------------------- 定义操作mysql函数 step1------------------------------
#------------------------------------------------------------------------------
def  mysqlexe(sql):
   db = MySQLdb.connect('localhost','root','djq002','python')
   cur = db.cursor()
   cur.execute(sql)
   result = cur.fetchall()
   db.commit()
   db.close()
   return result
   

#------------------------------------------------------------------------------
#---------------------- 创建从网页上获url的类 step2 --------------------------------
#------------------------------------------------------------------------------
class MParser(HTMLParser.HTMLParser):
    mvalue = [] 
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
               if name == 'href' and value.startswith('http') and value not in self.mvalue:   			        # 检查url是否以‘http’开头以及列表mvalue是否有重复的url
                    exclude = re.match(r".*(?=baidu|BAIDU|BaiDu).*",value) 					# 去除有关百度的url
		    if exclude ==None:
                       self.mvalue.append(value)


        



#if __name__ == '__main__':

#----------------------------------------------------------------------------
#--------------------------- 获取种子 step3--------------------------------------
#----------------------------------------------------------------------------
lo = 'y'
my = MParser()

while lo == 'y':
# 获取url并打开url进行数据读取
   url = raw_input('输入网址：')
   fdata1 = urllib2.urlopen(url).read()
   
   my.feed(fdata1)

# 获取mysql url 表里的所有记录，并加载到列表里面
   content1 = [] 
   result1 = mysqlexe('select url from url')
   for line in result1:      
       content1.append(line[0])
   print 
   print 'collecting !!'
   
   try:
       for surl in  my.mvalue:
	        if surl not in content1:	        
                   sql2 =  'insert into url(url) select'+' '+'\"'+surl+'\"'
	           mysqlexe(sql2)
               
       print 
       print 'done !!' 
       lo = raw_input('  want to again(y/n):')
       print
        
   except HTMLParser.HTMLParseError,e:
       print e

   
#----------------------------------------------------------------------------
#--------------------------- 搜索目标url step3------------------------------
#----------------------------------------------------------------------------

print
print 'hunting start!!'  


result2 = mysqlexe('select url from url')
for seed1  in result2:
   fdata2 = urllib2.urlopen(seed1[0]).read()
   myp = MParser()
   myp.feed(fdata2)
   for joburl in myp.mvalue:
       judge1 = re.match(r'.*(/hr\.|/hr/|/Hr|career|Career|/job\.|/Job\.|jobs|joinus|Joinus|/join/|join\.|Join|recruit|Recruit|zhaopin|ZhaoPin|zpxx|ZPXX|employer|Employer|campus|Campus|/school|/School|/yrln){1}.*',joburl)
       if judge1 != None:
           sql3 = 'insert into joburl(url) select'+' '+'\"'+joburl+'\"'
	   mysqlexe(sql3)
		   


print 'over!!'		   
print '------------------------ tansuozhe:djq002 -----------------------------'
print
print
		   
	   

	   
	   
	   
      

	   
