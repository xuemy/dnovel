# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy-0.16.org/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
    url = Field()
    content = Field()
    novel = Field()
    fetch = Field()
    order = Field()
    name = Field()
    #db = Field()
