# coding: utf-8
"""
    Извлекатель картинок из reddit.com/r/funny путем дерганья API
"""

import json
import urllib2
import re
import itertools
import datetime
import time

from linkmodel import Link

REDDIT_URL = 'http://reddit.com/r/funny.json?limit=100'


def wget(url):
    rq = urllib2.Request(url, headers={'User-Agent': 'pictures api-using bot by /u/babazka'})
    return urllib2.urlopen(rq).read()
        
def link_filter(links):
    link_must_contain_one_of = [
        '.png', '.gif', '.jpg', 'imgur.com'
    ]
    for link in links:
        for must_have in link_must_contain_one_of:
            if must_have in link.url.lower():
                yield link
                break
    
def parse_reddit():
    funny_json = wget(REDDIT_URL)
    funny = json.loads(funny_json)
    links = []
    for entity in funny['data']['children']:    
        date = datetime.datetime.fromtimestamp(entity['data']['created'])
        link = Link(entity['data']['url'], entity['data']['title'], date, 'http://reddit.com' + entity['data']['permalink'])
        links.append(link)
    links = list(link_filter(links))
    return links
    
