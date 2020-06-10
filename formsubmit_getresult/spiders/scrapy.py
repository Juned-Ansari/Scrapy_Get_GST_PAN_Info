# create project from terminal 
# scrapy startproject quotescss
import scrapy
import time 
import random
class LaughfactorySpider(scrapy.Spider):
    handle_httpstatus_list = [403, 504]
    name = "myjustdial"
    start_urls = ["https://www.justdial.com/Agra/Readymade-Garment-Retailers/nct-10401947/page-1"]

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    }

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], headers=self.headers)

    def parse(self,response):
        time.sleep(random.randint(0,4))
        for site in response.xpath("//section[@class='rslwrp ']/div/ul"):
            item = {
                'shopname': site.xpath("//li[@class='cntanr']/section//h2[@class='store-name']/span/a/span/text()").extract_first()
            }
            yield item

        next_page = response.xpath("//div[@id='srchpagination']/a/@href").extract_first(default='').strip()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, headers=self.headers, callback=self.parse)        
            