# coding utf-8
"""
    Сочиняет HTML-страницу по списку ссылок. Возвращает итератор по строкам.
"""
def make_page(links):
    yield '<html>'
    yield '<title>/r/funny</title>'
    yield '<ol>'
    for link in links:
        yield '<li><a href="%s">%s</a></li>' % (str(link.url), str(link.title))
    yield '</ol>'
    yield '</html>'
