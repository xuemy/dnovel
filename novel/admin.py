#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.contrib import admin

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

admin.site.register(Category,CategoryAdmin)
admin.site.register(Novel,NovelAdmin)
admin.site.register(Chapter,ChapterAdmin)
admin.site.register(SEO,SEOAdmin)
admin.site.register(Links,LinkAdmin)