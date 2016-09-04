#coding=utf8
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 09:46:45 2011

@author: Nupta
"""
import HTMLParser
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding("gb2312")     # 重新加载系统并设置默认编码


#------------------------------------------------------------------------------
#---------------------------- 连接到数据库 ----------------------------------
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#---------------------- 创建从网页上获url的类 --------------------------------
#------------------------------------------------------------------------------
class MParser(HTMLParser.HTMLParser):
    mvalue = [] 
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
                if name == 'href' and value.startswith('http') and value not in self.mvalue:
                    # exclude = re.match(r".*(?=baidu|BAIDU|BaiDu).*",value)
                    # if exclude ==None:
                        self.mvalue.append(value)
        
#	return mvalue


#if __name_ == '__main__':

#----------------------------------------------------------------------------
#--------------------------- 获取种子 --------------------------------------
#----------------------------------------------------------------------------

url=raw_input('输入网址：')
fdata=urllib2.urlopen(url).read()

my=MParser()
my.feed(fdata)



 
print '--------- sql execute results ---------'
print 
print
#for seeds in results:
for joburl in my.mvalue:
#   judge = re.search(r".*(hr|Hr)?(career|Career)?(job|Job)?(joinus|Joinus)?(join|Join)?(recruit|Recruit)?(zhaopin|ZhaoPin)?(zpxx|ZPXX)?(employer|Employer)?(campus|Campus)?(school|School).*",joburl)
   judge = re.match(r'.*(/hr\.|/hr/|/Hr|career|Career|/job\.|/Job\.|joinus|Joinus|/join/|join\.|Join|recruit|Recruit|zhaopin|ZhaoPin|zpxx|ZPXX|employer|Employer|campus|Campus|school|School){1}.*',joburl)
   while judge != None:
       print joburl
     
       break
   
  

#print results

print 


print
print  'done!!'






