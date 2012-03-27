# coding utf-8
"""
    Сочиняет HTML-страницу по списку ссылок. Возвращает итератор по строкам.
"""
def make_page(links):
    yield '<html>'
    yield '<title>/r/funny</title>'
    yield '<style>'
    yield 'li { margin-top: 16px; margin-bottom: 16px; }'
    yield '</style>'
    yield '<ol>'
    for link in links:
        yield '<li><a href="%s">%s</a></li>' % (link.url.encode('utf-8', 'replace'), link.title.encode('utf-8', 'replace'))
    yield '</ol>'
    yield '</html>'
