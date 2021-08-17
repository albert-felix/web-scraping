import scrapy
from ..items import SmartPhoneItem

class SmartPhones(scrapy.Spider):
    name = "smartphones"
    start_urls = [
        "https://www.amazon.in/s?k=iphone&i=electronics&rh=n%3A1389432031%2Cp_89%3AApple&dc&qid=1629199162&rnid=3837712031&ref=sr_pg_1"
    ]

    def parse(self, response):
        names = response.css('.a-size-medium.a-text-normal::text').extract()
        prices = response.css('#search .a-price-whole::text').extract()
        img_urls = response.css('.s-image::attr(src)').extract()
        items = SmartPhoneItem()
        for name, price, img_url in zip(names, prices, img_urls):
            items['name'] = name
            items['price'] = price  
            items['img_url'] = img_url
            yield items

        next_page = response.css('.a-pagination .a-last a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)