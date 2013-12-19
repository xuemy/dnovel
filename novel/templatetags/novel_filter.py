#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'meng'

from django import template

register = template.Library()

@register.filter(name = 'cut_list')
def cut_list(arr,n = 3):
    _t = None
    _arr = [arr[i:i+n] for i in range(0, len(arr), n)]
    for a in _arr:
        if len(a) != n:
            for _ in range(0,n - len(a)):
                a.append(_t)

    return _arr