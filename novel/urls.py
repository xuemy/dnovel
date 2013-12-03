#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static

__author__ = 'meng'

from django.conf.urls import patterns,url
from novel import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^cat/(?P<category_alias>[A-Za-z]+)/$',views.category,name='category'),
    url(r'^book/(?P<book_alias>[A-Za-z]+)/$',views.book,name='book'),
    url(r'^book/(?P<book_alias>[A-Za-z]+)/(?P<chapter_id>\d+)\.html$',views.chapter,name='chapter'),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT})
)