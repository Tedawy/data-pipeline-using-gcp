# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BayutScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    price = scrapy.Field()
    #developer = scrapy.Field()
    location = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    area = scrapy.Field()
    property_type = scrapy.Field()
    furnishing = scrapy.Field()
    completion_status = scrapy.Field()
    property_keywords= scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()


    """
    amenities = scrapy.Field()
    description = scrapy.Field()
    """
