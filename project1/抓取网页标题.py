#coding=utf8
from lxml import html

url = raw_input('input the url:')
doc = html.parse(url)
title = doc.find('.//title').text
print title
