#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
from django.utils import six
from django.utils.encoding import smart_unicode
from markupsafe import Markup
import re
from scrapy import log
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import  Join, TakeFirst
from scrapy.http import Request
from scrapy.item import Item,Field
from scrapy.selector import Selector
from scrapy.spider import BaseSpider
from novel.models import Collection, Novel, Category
from spider.items import ArticleItem
from config import type
__author__ = 'meng'



class LostLoader(XPathItemLoader):
    default_output_processor = Join("")
    novel_out = TakeFirst()
    order_out = TakeFirst()
    db_out = TakeFirst()

def slugify(value, substitutions=()):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    Took from Django sources.
    """
    # TODO Maybe steal again from current Django 1.5dev
    value = Markup(value).striptags()
    # value must be unicode per se
    import unicodedata
    from unidecode import unidecode
    # unidecode returns str in Py2 and 3, so in Py2 we have to make
    # it unicode again
    value = unidecode(value)
    if isinstance(value, six.binary_type):
        value = value.decode('ascii')
    # still unicode
    value = unicodedata.normalize('NFKD', value).lower()
    for src, dst in substitutions:
        value = value.replace(src.lower(), dst.lower())
    value = re.sub('[^\w\s-]', '', value).strip()
    value = re.sub('[-\s]+', '', value)
    # we want only ASCII chars
    value = value.encode('ascii', 'ignore')
    # but Pelican should generally use only unicode
    return value.decode('ascii')



class Lost(BaseSpider):
    name = 'lost'
    def __init__(self,*args, **kwargs):
        super(Lost, self).__init__(*args,**kwargs)
        self.config = kwargs.get('config',None)
        self.book = kwargs.get('book',None)

        if not self.book:
            self.bookname = kwargs.get('bookname')
            self.url = kwargs.get('url')
        if self.config in type:
            args = type[self.config]
            self.chapter_list = args.get('chapter_list',None)
            self.content = args.get('content',None)
            self.filters = args.get('filter',None)
            self.xpath_book = args.get('book',None)
            self.author = args.get('author',None)
            log.msg(args)
        else:
            log.msg(u"配置文件不正确")
            return


    def parse(self, response):
        if not self.book:
            log.msg("小说不在数据库中，下面创建小说")
            log.msg("获取小说标题和作者")
            hxs = Selector(response)
            join = Join("")
            _book = hxs.xpath(self.xpath_book).extract()
            if self.author:
                _author = hxs.xpath(self.author).extract()
                author = join(_author)
            else:
                author = ""
            book = join(_book) or None
            log.msg("插入小说到数据库中")
            novel = Novel(name = book,author = author,spider_class = self.config,start_url = self.url,interval = 10,alias=slugify(book))
            category = Category.objects.all()
            novel.category = category[0]
            novel.save()
            log.msg("插入小说成功")
            self.book = novel

        if self.chapter_list:
            log.msg(u"开始获取章节列表")
            _sgml = SgmlLinkExtractor(restrict_xpaths=self.chapter_list)
            links = _sgml.extract_links(response)
            log.msg(u"成功获取章节列表")

            for n,link in enumerate(links,start=1):
                _q = Collection.objects.filter(url_hash = hashlib.sha1(link.url).hexdigest())
                if not _q:
                    yield Request(url=link.url,callback=self._parse,meta=dict(link = link,num = n))
        else:
            log.msg(u"没有获取到章节列表的XPATH,请修改配置文件")
            return

    def _parse(self,response):
        hxs = Selector(response)
        meta = response.meta
        c = hxs.xpath(self.content).extract()

        l = LostLoader(item=ArticleItem(),response = response)
        l.add_value('url',response.url)
        l.add_value('name',meta['link'].text,Join(""),self._Filter(self.filters))
        l.add_value('content',['<p>%s</p>'%cc for cc in c],Join(),self._Filter(self.filters))
        l.add_value('order',int(str(self.book.id) +'100' + str(meta['num'])))
        l.add_value('novel',self.book)
        return l.load_item()

    class _Filter(object):
        def __init__(self,f):
            self.filters = f
        def __call__(self, content):
            for filter in self.filters:
                #log.msg(content[:100])
                content = content.replace(smart_unicode(filter),u"")
            return content

#class TestItem(Item):
#    url = Field()
#
#class Test(BaseSpider):
#    name = 'test'
#    start_urls = ['http://www.fftxt.net/book/4837/']
#
#    def __init__(self, *args, **kwargs):
#        super(Test, self).__init__(*args, **kwargs)
#        self.s = kwargs['sett']
#    def parse(self, response):
#        args = type['fftxt']
#        self.chapter_list = args.get('chapter_list',None)
#        self.content = args.get('content',None)
#        self.filters = args.get('filter',None)
#        self.xpath_book = args.get('book',None)
#        self.author = args.get('author',None)
#        _sgml = SgmlLinkExtractor(restrict_xpaths=self.chapter_list)
#        links = _sgml.extract_links(response)[:10]
#        items = []
#        for n,link in enumerate(links,start=1):
#            i = TestItem()
#            i['url'] = dict(url = link.url,s = self.s['USER_AGENTS'])
#            items.append(i)
#        return items
#            #yield Request(url=link.url,callback=self._parse,meta=dict(link = link,num = n))
#    def _parse(self,response):
#        hxs = Selector(response)
#        meta = response.meta
#        c = hxs.xpath(self.content).extract()
#
#        l = LostLoader(item=ArticleItem(),response = response)
#        l.add_value('url',response.url)
#        l.add_value('name',meta['link'].text,Join(""),self._Filter(self.filters))
#        l.add_value('content',['<p>%s</p>'%cc for cc in c],Join(),self._Filter(self.filters))
#        l.add_value('order',int(100))
#        l.add_value('novel','book')
#        return l.load_item()
#    class _Filter(object):
#        def __init__(self,f):
#            self.filters = f
#        def __call__(self, content):
#            for filter in self.filters:
#                log.msg(content[:100])
#                content = content.replace(smart_unicode(filter),u"")
#            return content


