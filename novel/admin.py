#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render_to_response

__author__ = 'meng'


from novel.models import Category,Novel, Chapter, SEO, Links


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class NovelAdmin(admin.ModelAdmin):
    list_display = ('name','author','category')

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name','novel')
class SEOAdmin(admin.ModelAdmin):
    pass
class LinkAdmin(admin.ModelAdmin):
    pass


def my_view(request, *args, **kwargs):
    return render_to_response('404.html')
admin.site.register_view('my_view', view=my_view,name="crontab")
admin.site.register(Category,CategoryAdmin)
admin.site.register(Novel,NovelAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(SEO,SEOAdmin)
admin.site.register(Links,LinkAdmin)