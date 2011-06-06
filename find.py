#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2
import re

class FindCrack(object):
	'''
	search cracks on http://mskd-ru.net
	''''
	def __init__(self):
		self.result = []
		
	def search(self,name,count=1000):
		'''
		name = name program
		count = number result, default - 1000
		''''
		page = urllib2.urlopen('http://mskd-ru.net/apteka.php?crack=%s' % name).read()
		self.parse(page)
		return self.result[:int(count)]
		
	def parse(self,html):
		for j in re.findall(r'(<a target=_blank href="\./redir.php\?(.*?)">(.*?)</a>\s::\s(.*?)\s::\s(.*?)<br>)',html):
			res = list(j)
			self.result.append(dict(url=res[1],name=res[2],size=res[3],date=res[4]))
'''		
example use this class
find = FindCrack()
for cr in find.search('decompiler',10):
	print cr
'''