#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'meng'

class Row(dict):
    def __getattr__(self,name):
        try:
            return self[name]
        except KeyError:
            raise  AttributeError(name)


type = Row(
    {
        '22mt': Row({
            "site_name": "墨坛文学",
            "site_url": "http://www.22mt.com/",
            "chapter_list": "//div[@class='book_listtext']",
            "content": "//div[@id='booktext']/text()",
            "filter": ["/墨坛文学", "墨坛文学网"]
        }),
        'fftxt':Row({
            "site_name":"非凡文学",
            "site_url":"http://www.fftxt.net/",
            "book":"//div[@class='book_news_style_text2']/h1/text()",
            "author":"",
            "chapter_list":"//ul[@id='chapterlist']/li",
            "content":"//div[@class='novel_content']/text()",
            "filter":["非凡TXT下载","www.fftxt.net"]
        }),
    }
)
