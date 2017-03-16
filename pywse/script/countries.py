# -*- coding:utf-8 -*-

from html.parser import HTMLParser
import requests
from collections import OrderedDict
import json

countries = ['Brazil', ]
url = 'https://en.wikipedia.org/wiki/%s'

class CountriesHtml(HTMLParser):

    find_capital = 0
    kwargs = {}

    def handle_starttag(self,tag,attr):
        if tag == 'table':
            self.find_capital = 1

        if self.find_capital == 1 and tag == 'td':
            self.find_capital = 2

        if self.find_capital == 3 and tag == 'a':
            self.find_capital = 4

    def handle_endtag(self,tag):
        pass

    def handle_data(self,data):
        data = data.strip()
        if self.find_capital == 4:
            self.kwargs['capital'] = data.decode('utf=8')
            self.find_capital = -float('Inf')
        if self.find_capital == 2:
            if data == 'Capital':
                self.find_capital = 3

    def __str__(self):
        result = OrderedDict()
        for arg in ('name', 'state', 'demonym', 'language', 'currency', 'capital'):
            result[arg] = '{%s}' % (arg)
            if not arg in self.kwargs:
                self.kwargs[arg] = ''
        result = json.dumps(result)
        result = result[1:-1]
        result = unicode(result)
        result = result.format(**self.kwargs)
        result = '{' + result + '}'
        return result.encode('utf-8')

if __name__ == '__main__':
    for country in countries:
        c_url = url % (country)
        r = requests.get(c_url)
        countries_html = CountriesHtml()
        countries_html.feed(r.content)
        print countries_html