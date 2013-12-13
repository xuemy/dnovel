#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from novel.models import SEO, Category, Novel, Chapter
from django.views.decorators.gzip import gzip_page
__author__ = 'meng'

@gzip_page
def index(request):
    """

    :param request:
    :return:
    """
    #定义一个字典 保存模板变量
    # 从SEO表中取出 index_book
    index = SEO.objects.all()
    if index:
        index_book = index[0].index_book
    # 获取章节列表
        chapter = index_book.chapter_set.all()

        template_var = dict(
            index_book = index_book,
            chapter = chapter,
        )
        return render_to_response('index.html',template_var,context_instance=RequestContext(request))
    else:
        return  HttpResponse("请在后台选择一本小说")

@gzip_page
def category(request,category_alias):
    """

    :param request:
    """
    #获取 该 分类下的所有小说
    novel_list = get_object_or_404(Category,alias = category_alias).novel_set.all()
    template_var = dict(
        novel_list = novel_list,
        category_alias = category_alias
    )
    return render_to_response('category.html',template_var,context_instance=RequestContext(request))
    #return HttpResponse('ok')
@gzip_page
def book(request,book_alias):
    '''
    小说详情页（章节页）
    '''

    novel = get_object_or_404(Novel,alias = book_alias)
    template_var = dict(
        novel = novel,
        chapter_list = novel.chapter_set.all()
    )
    return render_to_response('book.html',template_var,context_instance=RequestContext(request))
    #return HttpResponse('ok')
@gzip_page
def chapter(request,book_alias,chapter_id):
    '''
    章节页
    '''
    book = get_object_or_404(Novel,alias = book_alias)
    chapter = get_object_or_404(Chapter,novel = book,order = chapter_id)
    return render_to_response('chapter.html',{'chapter':chapter,'book':book},context_instance=RequestContext(request))
    #return HttpResponse('ok')