import scrapy
import json 
from bayut_scraper.items import BayutScraperItem
from urllib.parse import urljoin
import re 

class BayutSpider(scrapy.Spider):
    name = "bayut"

    def start_requests(self):
        """
        cities = ['dubai', 'abu-dhabi','sharjah','ajman',
                 'ras-al-khaimah', 'umm-al-quwain', 'al-ain', 'fujairah'] # for further analysis
        for city in cities:
            URL = f"https://www.bayut.com/for-sale/property/{city}/"
            yield scrapy.Request(url=URL, callback=self.parse,)
        """
        
        URL = f"https://www.bayut.com/for-sale/property/dubai/" 
        yield scrapy.Request(url=URL, callback=self.parse,)   

    def parse(self, response):
        
        properties = response.css("li.ef447dde")

        for property in properties:
            #data = BayutScraperItem()
            #data['developer'] = property.css("img._062617f4.lazy:not([data-src])::attr(alt), img._062617f4::attr(alt)").getall()
            info = property.css("div._4041eb80 a::attr(href)").get()
            if info:
                 yield response.follow(info, callback=self.parse_property_page,)# meta={'item': data})

        next_page = response.css('a[title="Next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)



    def parse_property_page(self,response):
        #data = response.meta['item']  # Retrieve item from meta
        data = BayutScraperItem()
        info = response.css('div._6803f627')

        data["price"] = info.css("div.c4fc20ba span[aria-label='Price'] ::text").get() 
        data['location'] = info.css("div._1f0f1758 ::text").get()
        data['bedrooms'] = info.css("span.fc2d1086 ::text").get()
        data['bathrooms'] = info.css('span[aria-label="Baths"] ::text').get()
        data['area'] = info.css('span[aria-label="Area"] ::text').get()
        data['property_type'] = info.css('span._812aa185 ::text').get()
        data['furnishing'] = info.css('span[aria-label="Furnishing"] ::text').get()
        data['completion_status'] = info.css('span[aria-label="Completion status"] ::text').get()
        data['property_keywords'] = info.css('h1.fcca24e0 ::text').get()


        scripts = info.css("script[type='application/ld+json']").getall()

        geo_script = None
        for script in scripts:
            if '"@type":"Apartment"' in script:
                geo_script = script
                break

        if geo_script:
            # Extract longitude and latitude using regex
            longitude = re.search(r'"longitude":\s*([\d.-]+)', geo_script)
            latitude = re.search(r'"latitude":\s*([\d.-]+)', geo_script)

            if longitude and latitude:
                data['longitude'] = longitude.group(1)
                data['latitude'] = latitude.group(1)
                
            else:
                self.logger.error("Longitude or latitude not found in the script.")
        else:
            self.logger.error("Geo script not found on the page.")
        
        # For further analysis and machine learning 
        #data['amenities'] = info.css('span._005a682a ::text').getall()
        #data['description'] = info.css('span._2a806e1e ::text').getall()

        yield data