#encoding:utf-8
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy-0.16.org/topics/item-pipeline.html

import hashlib
import json
from novel.models import Chapter, Collection
'''
    url = Column(Unicode(255))
    url_hash = Column(Unicode(20),unique=True)
    nid = Column(Integer)
    nname = Column(Unicode(50))
    cid = Column(Integer)
    cname = Column(Unicode(50))
'''
class CollectionPipeline(object):

    def process_item(self,item,spider):
        novel = item['novel']
        #db = item['db']
        #db.execute('INSERT INTO novel_chapter(name,content,order) VALUES ')
        chapter = Chapter(
                    name = item['name'],
                    content = item['content'],
                    order = item['order'])
        chapter.novel = novel
        collection = Collection(
            url = item['url'],
            url_hash = hashlib.sha1(item['url']).hexdigest(),
            name = item['name'],
            book = novel.name
        )
        collection.novel = novel
        chapter.save()
        collection.save()

class TestPipeline(object):
    def __init__(self):
        self.file = open('test.json','wb')
    def process_item(self,item,spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line)
        return item