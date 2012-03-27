# coding: utf-8
"""
    Извлекатель картинок из reddit.com/r/funny путем парсинга HTML
"""


import urllib2
import re
import itertools
import dateutil.parser
import time

from linkmodel import Link

MAX_LINKS = 70
REDDIT_URL = 'http://reddit.com/r/funny'
PAGE_SLEEP = 3.0

rLink = re.compile('<a class="title " href="([^"]+)" >(.*?)</a>')
rTime = re.compile('<time title="[^"]+" datetime="([^"]+)">')
rNextPage = re.compile("<a href=\"(http://www.reddit.com/r/funny/.count=[0-9]+&[^\"]*after=[^\"]*?)\"")




class RateController(object):
    """
        Штука, ограничивающая частоту запросов к серверу.
        Надо вызывать check() перед каждым запросом;
        если понадобится, штука заставит заснуть.
    """
    def __init__(self, min_interval):
        self.min_interval = min_interval
        self.next_allowed_t = time.time()
    
    def check(self):
        now = time.time()
        dt = self.next_allowed_t - now
        if dt > self.min_interval:
            time.sleep(dt)
        self.next_allowed_t = time.time() + self.min_interval
        
rate_controller = RateController(min_interval=3.0)

def wget(url):
    rq = urllib2.Request(url, headers={'User-Agent': 'pictures bot by /u/babazka'})
    return urllib2.urlopen(rq).read()
        
def parse_page(url):
    page = wget(url)
    links = rLink.findall(page)
    times = rTime.findall(page)
    link_objs = []
    
    for ((href, title), time) in itertools.izip(links, times):
        time = dateutil.parser.parse(time)
        link_objs.append(Link(href, title, time))
    
    print len(links), len(times)
    next_page = rNextPage.findall(page)
    if next_page:
        next_page = next_page[0]
        
    return link_objs, next_page
    
def link_filter(links):
    link_must_contain_one_of = [
        '.png', '.gif', '.jpg', 'imgur.com'
    ]
    for link in links:
        for must_have in link_must_contain_one_of:
            if must_have in link.url.lower():
                yield link
                break
    
def parse_many_pages():
    url = REDDIT_URL
    links = []
    while url and len(links) < MAX_LINKS:
        print 'parsing', url
        rate_controller.check()
        new_links, next_page = parse_page(url)
        new_links = link_filter(new_links)
        url = next_page
        links.extend(list(new_links))
    print len(links)
    return links
    
parse_reddit = parse_many_pages
