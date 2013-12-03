#!/usr/bin/python
# -*- coding: utf-8 -*-
from novel.models import Category, SEO, Links

__author__ = 'meng'


def my_processor(request):
    seo = SEO.objects.all()
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

        )
    else:
        return dict(
            category_list = Category.objects.all(),
            link_list = Links.objects.all(),
        )