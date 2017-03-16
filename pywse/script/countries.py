# -*- coding:utf-8 -*-

from html.parser import HTMLParser
import requests
from collections import OrderedDict
import json
import time

countries = ['Brazil', ]
url = 'https://en.wikipedia.org/wiki/%s'

DEBUG = False

class CountriesHtml(HTMLParser):

    conditions = {
        'capital': {
            'condition': [
                {'<data>': 'Capital'},
                {'tag': 'a'},
                {'tag': 'td'},
                {'tag': 'table'},
            ],
            'value': '',
            'value_index': 2,
        },
        'demonym': {
            'condition': [
                {'<data>': 'Demonym'},
                {'tag': 'a'},
                {'tag': 'td'},
                {'tag': 'table'},
            ],
            'value': '',
            'value_index': 2,
        },
        'language': {
            'condition': [
                {'<data>': 'languages'},
                {'tag': 'a'},
                {'tag': 'td'},
                {'tag': 'table'},
            ],
            'value': '',
            'value_index': 2,
        },
        'currency': {
            'condition': [
                {'<data>': 'Currency'},
                {'tag': 'a'},
                {'tag': 'td'},
                {'tag': 'table'},
            ],
            'value': '',
            'value_index': 2,
        },
    }

    find_capital = 0
    kwargs = { 'state': '' }
    states = ['North America', 'South America', 'Asia', 'Africa', 'Europe', 'Oceania']

    def pop_condition(self, arg):
        if not arg in self.conditions:
            return
        condition = self.conditions[arg]['condition']
        last_dict = condition.pop()
        if '<data>' in last_dict:
            self.kwargs[arg] = self.conditions.pop(arg)['value_index']

    def handle_starttag(self,tag,attr):
        for arg in self.conditions.keys():
            condition = self.conditions[arg]['condition'][-1]
            if 'tag' in condition:
                self.pop_condition(arg=arg)

    def handle_endtag(self,tag):
        pass

    def set_state(self, data):
        if self.kwargs['state'] is '':
            for state in self.states:
                if state in data:
                    self.kwargs['state'] = state

    def handle_data(self,data):

        data = data.strip()
        if data:
            self.set_state(data=data)

        for arg in self.kwargs:
            if isinstance(self.kwargs[arg], int):
                self.kwargs[arg] -= 1
                if DEBUG is True:
                    print arg, data.decode('utf=8'), self.kwargs[arg]
                if self.kwargs[arg] is 0:
                    self.kwargs[arg] = data.decode('utf=8')

        for arg in self.conditions.keys():
            condition = self.conditions[arg]['condition'][-1]
            if '<data>' in condition:
                if data == condition['<data>']:
                    self.kwargs[arg] = None
                    self.pop_condition(arg=arg)

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
        result = '    {' + result + '}'
        return result.encode('utf-8')

if __name__ == '__main__':
    for country in countries:
        c_url = url % (country)
        r = requests.get(c_url)
        countries_html = CountriesHtml()
        countries_html.feed(r.content)
        countries_html.kwargs['name'] = country
        print countries_html
        time.sleep(1)