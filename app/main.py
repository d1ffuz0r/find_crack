#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from re import findall, I
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class FindCrack(object):
    '''
    search cracks on mskd-ru.net,www.crackserialkeygen.com,andr.net,keygens.nl,www.supercracks.net
    '''
    def __init__(self):
        self.result = []
        self.__all__ = [
                        {
                            'url':'http://mskd-ru.net/apteka.php?crack=%s',
                            'prefix':'',
                            'regexp':r'<a target=_blank\shref="\./redir.php\?(.*?)"\s(.*?)>(.*?)</a>\s::(.*?)\s::\s(.*?)<br>',
                            'rows':[0, 2],
                        },
                        {
                            'url':'http://www.crackserialkeygen.com/%s-crack-serial-keygen.html',
                            'prefix':'http://www.crackserialkeygen.com',
                            'regexp':r'<div class="result"><a class="slink" href="(.*?)">(.*?)</a>',
                            'rows':[0, 1],
                        },
                        {
                            'url':'http://andr.net/search.php?stype=andrnet&str=%s',
                            'prefix':'http://andr.net/d.php?c=',
                            'regexp':r'<td width="520">(.*?)<a href="javascript:(c2|c)\((\d+)\)" >\s(.*?)</a><br></td>',
                            'rows':[2, 3],
                        },
                        {
                            'url':'http://keygens.nl/cracked_warez_search.php?s=%s',
                            'prefix':'http://keygens.nl',
                            'regexp':r'<a href="(.*?/crack/.*?)">(.*?)</a><br>',
                            'rows':[0, 1]
                        },
                        {
                            'url':'http://www.supercracks.net/search.php?crack=%s',
                            'prefix':'http://www.supercracks.net/v.php?id=',
                            'regexp':r'<a href="javascript:download\((\d+)\);">(.*?)</a><br>',
                            'rows':[0, 1]
                        },
                    ]
        
    def search(self, name, count=1000):
        map(lambda param:self._parse(param, name), self.__all__)
        return self.result[:int(count)]
        
    def _parse(self, data, name):
        page = fetch(data['url'] % name).content
        for res in findall(data['regexp'], page, I):
            self.result.append(dict(url=data['prefix'] + res[data['rows'][0]], name=res[data['rows'][1]]))
            
finder = FindCrack()

class Main(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path,()))

class Find(webapp.RequestHandler):
    def post(self):
        if self.request.get('application'):
            out = ''
            res = finder.search(self.request.get('application'))
            for res in res:
                out += '<a href="%s">%s</a><br/>' %(res['url'], res['name'])
        else:
            out = '<h1>Произошла ошибка или вы не ввели название приложения</h1>'
        self.response.out.write(out)

application = webapp.WSGIApplication([('/', Main), ('/find', Find)], debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()