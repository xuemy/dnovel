#encoding:utf-8
from django.db import models
# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from tinymce.models import HTMLField


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=100,unique=True)

    @property
    def get_category_url(self):
        return '/cat/%s' % self.alias
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Novel(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(u"小说名",max_length=100,db_index=True)
    alias = models.CharField(u"小说拼音",max_length=100,unique=True,db_index=True,blank=True)
    author = models.CharField(u'作者',max_length=50,blank=True)
    description = models.TextField(u"小说简介",blank=True)
    #last_chapter = models.CharField(u'最新更新章节',max_length=)
    is_over = models.BooleanField(u"小说是否完结",blank=True)
    image = models.ImageField(u"封面图片",upload_to='novel_cover',max_length=255,blank=True)
    hot = models.IntegerField(db_index=True,default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    start_url = models.CharField(u"采集起始URL",max_length=255,blank=True)
    spider_class = models.CharField(u"采集类",max_length=20,blank=True)
    interval = models.SmallIntegerField(u"采集间隔",blank=True)

    seo_title = models.CharField(u"SEO标题",max_length=255,blank=True)
    seo_keyword = models.CharField(u"SEO关键字",max_length=255,blank=True)
    seo_description = models.TextField(u"SEO描述",blank=True)

    @property
    def last_chapter(self):
        return self.chapter_set.order_by('-order')[0] or None
        #return self.chapter.
    @property
    def get_novel_url(self):
        return '/book/%s' % self.alias

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-hot']
@python_2_unicode_compatible
class Chapter(models.Model):
    novel = models.ForeignKey(Novel,db_index=True)
    name = models.CharField(r'章节名',max_length=255)
    content = HTMLField(u'内容')
    volume = models.SmallIntegerField(default=1)
    volume_name = models.CharField(max_length=50,default=u'正文')
    order = models.IntegerField(unique=True,db_index=True)
    update_time = models.DateTimeField(auto_now=True)

    @property
    def get_chapter_url(self):
        return '/book/%s/%s.html' %(self.novel.alias,self.order)
    @property
    def next_chapter(self):
        next = Chapter.objects.filter(novel=self.novel,order__gt = self.order).order_by('order')
        return next[0].get_chapter_url if next else ""
    @property
    def prev_chapter(self):
        prev = Chapter.objects.filter(novel=self.novel,order__lt = self.order).latest('order')
        return prev.get_chapter_url if prev else ""

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['order']
        index_together = [
            ['novel','order']
        ]


@python_2_unicode_compatible
class SEO(models.Model):
    index_book = models.OneToOneField(Novel)
    index_seo_title = models.CharField(u'网站首页SEO标题',max_length=100,blank=True)
    index_seo_keywords = models.CharField("首页seo关键字",max_length=255,blank=True)
    index_seo_description = models.CharField("首页seo描述",max_length=255,blank=True)
    site_name = models.CharField(u'网站名',max_length=50,blank=True)
    site_sub_name = models.CharField(u'网站副标题',max_length=100,blank=True)
    tongji = models.TextField(u'统计代码',blank=True)
    google = models.CharField(u'google统计ID',max_length=20,blank=True)

    def __str__(self):
        return self.index_book.name

@python_2_unicode_compatible
class Links(models.Model):
    name = models.CharField(u'网站名',max_length=50)
    url = models.CharField(u'网站URL',max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Collection(models.Model):
    novel = models.ForeignKey(Novel)
    book = models.CharField(max_length=40)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    url_hash = models.CharField(max_length=40,db_index=True)

    def __str__(self):
        self.name
