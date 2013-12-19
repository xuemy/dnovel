#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static

__author__ = 'meng'

from django.conf.urls import patterns,url
from novel import views

urlpatterns = patterns('',
    url(r'^$',views.index,name='index'),
    url(r'^(?P<category_alias>[A-Za-z]+)/$',views.category,name='category'),
    url(r'^book/(?P<book_alias>[A-Za-z]+)/$',views.book,name='book'),
    url(r'^book/(?P<book_alias>[A-Za-z]+)/(?P<chapter_id>\d+)\.html$',views.chapter,name='chapter'),
    url(r'^book/(?P<book_alias>[A-Za-z]+)/download/$',views.book_download,name="novel_download"),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),

    url(r'^temp_test$',views.temp_text)
)