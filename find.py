#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2
import re

class FindCrack(object):
	'''
	search cracks on http://mskd-ru.net,www.crackserialkeygen.com
	'''
	def __init__(self):
		self.result = []
		self.__all__ = [
					{
						'url':'http://mskd-ru.net/apteka.php?crack=%s',
						'regexp':r'<a target=_blank\shref="\./redir.php\?(.*?)"\s(.*?)>(.*?)</a>\s::(.*?)\s::\s(.*?)<br>',
						'rows':[0, 2]
					},
					{
						'url':'http://www.crackserialkeygen.com/%s-crack-serial-keygen.html',
						'regexp':r'<div class="result"><a class="slink" href="(.*?)">(.*?)</a>',
						'rows':[0, 1]
					}
				]
		
	def search(self, name, count=1000):
		'''
		name = name what search
		count = number result, default - 1000
		'''
		map(lambda param:self._parse(param, name), self.__all__)
		return self.result[:int(count)]
		
	def _parse(self, data, name):
		page = urllib2.urlopen(data['url'] % name).read()
		for res in re.findall(data['regexp'], page, re.I):
			self.result.append(dict(url=res[data['rows'][0]], name=res[data['rows'][1]]))

'''
example
find = FindCrack()
for j in find.search('decompiler', 10):
	print j
'''
