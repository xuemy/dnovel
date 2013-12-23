#!/usr/bin/python
# -*- coding: utf-8 -*-
from novel.models import Category, SEO, Links,Novel

__author__ = 'meng'


def my_processor(request):
    seo = SEO.objects.all()
    random_novel = Novel.objects.order_by("?")
    if random_novel:
        random_novel = random_novel[:10]
    else:
        random_novel = None
    if seo:
        seo = seo[0]
        return dict(
            category_list = Category.objects.all(),
            site_name = seo.site_name,
            site_sub_name = seo.site_sub_name,
            tongji = seo.tongji,
            google = seo.google,
            link_list = Links.objects.all(),
            seo = seo,
            random_novel = random_novel,
            site_url = seo.site_url

        )
    else:
        return dict(
            category_list = Category.objects.all(),
            link_list = Links.objects.all(),
        )