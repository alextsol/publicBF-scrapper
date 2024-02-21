# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MyItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()

class publicItems(scrapy.Item):
    name = scrapy.Field()
    category = scrapy.Field()
    started_price = scrapy.Field()
    current_price = scrapy.Field()
    discounted_amount = scrapy.Field()
    discount_percentage = scrapy.Field()
    product_link = scrapy.Field()
    date = scrapy.Field()
