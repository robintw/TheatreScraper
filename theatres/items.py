# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class TheatresItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    date = Field()
    desc = Field()
    start = Field()
    end = Field()
    url = Field()
    location = Field()
