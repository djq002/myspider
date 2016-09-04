#coding=utf8
from HTMLParser import HTMLParser
import  MySQLdb
import  re

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
   
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++  构造字典  ++++++++++++++++++++++++++++++++++++++++++++++
table_list = {}

# 将sql查询结果加载到字典上
m = 1
print '数据库有以下数据表可供选择：'
print 
print '键名','   '，'表'
for line1 in mysqlexe('show tables'):
    # 符合条件的才加载 
   match1 = re.match(r'link{1}.*',line1[0])
   if match1!=None:
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

sql = 'select * from  '+select_table
print mysqlexe(sql) 

