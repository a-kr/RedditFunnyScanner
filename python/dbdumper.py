# coding: utf-8
"""
    Скрипт сливает ссылки с реддита и заливает в БД
"""

import os
import sqlite3

import apireader

FILENAME = os.path.join(os.path.dirname(__file__), 'reddit.db3')

def db_init():
    conn = sqlite3.connect(FILENAME)
    conn.execute('''
        CREATE TABLE links (url TEXT, title TEXT, date TIMESTAMP, comments TEXT);
    ''')
    conn.execute('''
        CREATE UNIQUE INDEX links_url ON links(url);
    ''')
    conn.close()

def get_connection():
    if not os.path.isfile(FILENAME):
        db_init()
    conn = sqlite3.connect(FILENAME)
    return conn
    
def fetch_and_dump():
    conn = get_connection()
    cur = conn.cursor()
    
    links = apireader.parse_reddit()
    for link in links:
        cur.execute('''SELECT rowid FROM links WHERE url = ?''', [link.url])
        rows = cur.fetchall()
        if len(rows) == 0:
            cur.execute('''INSERT INTO links (url, title, date, comments) VALUES (?, ?, ?, ?)''', [link.url, link.title, link.time, link.comments])
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    fetch_and_dump()
    