# coding: utf-8

import os
import sqlite3

FILENAME = os.path.join(os.path.dirname(__file__), 'reddit.db3')

class Link(object):
    def __init__(self, url, title, time, comments=""):
        self.url = url
        self.title = title
        self.time = time
        self.comments = comments
        
    def __repr__(self):
        return "Link(%s, %s, %s)" % (repr(self.url), repr(self.title), repr(self.time))
        
    @classmethod
    def select_all(_cls, limit=100):
        conn = sqlite3.connect(FILENAME)
        cur = conn.cursor()
        cur.execute('''SELECT url, title, date, comments FROM links ORDER BY date DESC LIMIT %d''' % limit)
        links = []
        for row in cur:
            link = Link(*row)
            links.append(link)
        conn.close()
        return links
