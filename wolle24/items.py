# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose, Identity, TakeFirst
import scrapy


class Wolle24Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field(
        input_processor=Identity(),
        output_processor=TakeFirst(),
    )
    product_brand = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    product_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    product_price = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    product_price_currency = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    product_delivery = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    product_needle_size = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
    product_material = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst())
