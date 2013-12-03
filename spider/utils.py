#!/usr/bin/python
# -*- coding: utf-8 -*-
import importlib


__author__ = 'meng'


from hashlib import sha1
try:
    import cPickle as pickle
except:
    import pickle



def filter_content(content,filters):
    for f in filters:
        if not isinstance(f,unicode):
            f = unicode(f,'utf-8')
        content = content.replace(f,u'')
    return content

def dumps(obj):
    return pickle.dumps(obj)
def loads(str):
    return pickle.loads(str)
def load_class(full_class_string):
    """
    dynamically load a class from a string
    """

    class_data = full_class_string.split(".")
    module_path = ".".join(class_data[:-1])
    class_str = class_data[-1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return getattr(module, class_str)
#print filter_content(u'\u7b2c\u5341\u4e00\u7ae0 \u89c1\u795e\u738b/\u58a8\u575b\u6587\u5b66',[u'/\u58a8\u575b\u6587\u5b66', u'\u58a8\u575b\u6587\u5b66'])