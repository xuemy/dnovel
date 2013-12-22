#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from functools import wraps
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from novel.models import SEO, Category, Novel, Chapter
from django.views.decorators.gzip import gzip_page
import os,codecs,mimetypes
__author__ = 'meng'

#@gzip_page
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
        template_var = dict(
            novel = index_book,
            chapterlist = index_book.get_novel_chapter,
            slug = "index"
        )
        return render_to_response('index.html',template_var,context_instance=RequestContext(request))
    else:
        return  HttpResponse("请在后台选择一本小说")

#@gzip_page
def category(request,category_alias):
    """

    :param request:
    """
    #获取 该 分类下的所有小说
    category_object = get_object_or_404(Category,alias = category_alias)
    novel_list = category_object.novel_set.all()

    template_var = dict(
        novel_list = novel_list,
        category_alias = category_alias,
        category = category_object,
        slug = "category"
    )
    return render_to_response('category.html',template_var,context_instance=RequestContext(request))

#@gzip_page
def book(request,book_alias):
    '''
    小说详情页（章节页）
    '''

    novel_object = get_object_or_404(Novel,alias = book_alias)
    template_var = dict(
        novel = novel_object,
        chapterlist = novel_object.get_novel_chapter,
        slug = "book"
    )
    return render_to_response('book.html',template_var,context_instance=RequestContext(request))
    #return HttpResponse('ok')

def book_download(request,book_alias):
    t = request.GET.get('type')
    def readFile(f, buf_size=262144):
        #f = open(fn, "rb")
        while True:
            c = f.read(buf_size)
            if c:
                yield c
            else:
                break
        f.close()
    def fileDownload(file_path):
        ''''''
        file_content_type = mimetypes.guess_type(file_path)[0]
        file_object = default_storage.open(file_path)
        response = HttpResponse(readFile(file_object),content_type=file_content_type)
        response['Content-Disposition'] = 'attachment; ' + filename_header
        response['Content-Length'] = default_storage.size(file_path)
        return response
    if t:
        novel_object = get_object_or_404(Novel,alias = book_alias)
        chapterlist = novel_object.chapter_set.all()
        _chapter = [dict(name = chapter.name,content = chapter.content.replace(u'<p>',"").replace(u"</p>","\n")) for chapter in chapterlist]
        if t == 'txt':
            from dnovel.settings import NOVEL_DOWNLOAD_ROOT
            file_name = book_alias + '.txt'
            file_path = os.path.join(NOVEL_DOWNLOAD_ROOT,file_name)

            filename_header = 'filename=%s' % file_name.encode('utf-8')

            content_str = ""
            for c in _chapter:
                content_str += '''{name}\n{content}\n'''.format(name = c['name'],content = c['content'])

            if default_storage.exists(file_path):
                #application/octet-stream
                #file_content_type = mimetypes.guess_type(file_path)[0]
                #file_object = default_storage.open(file_path)
                #response = HttpResponse(readFile(file_object),content_type=file_content_type)
                #response['Content-Disposition'] = 'attachment; ' + filename_header
                #response['Content-Length'] = default_storage.size(file_path)
                response = fileDownload(file_path)
                return response
            else:
                save_file = default_storage.save(file_path,ContentFile(content_str))
                response = fileDownload(file_path)
                return response
    else:
        return render_to_response("download.html",{})
#@gzip_page
def chapter(request,book_alias,chapter_id):
    '''
    章节页
    '''
    book = get_object_or_404(Novel,alias = book_alias)
    chapter = get_object_or_404(Chapter,novel = book,order = chapter_id)
    return render_to_response('chapter.html',{'chapter':chapter,'novel':book,'slug':"chapter",'category':book.category},context_instance=RequestContext(request))
    #return HttpResponse('ok')

def temp_text(request):
    return render_to_response("test.html",context_instance=RequestContext(request))