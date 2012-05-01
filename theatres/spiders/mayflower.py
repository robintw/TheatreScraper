from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from theatres.items import *


class MayflowerSpider(BaseSpider):
    name = "mayflower"
    allowed_domains = ["mayflower.org.uk"]
    start_urls = ["http://www.mayflower.org.uk/whatson.asp"]
    
    location = "Mayflower Theatre"

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        detail_urls = hxs.select("//a[@class='woTitle']/@href").extract()
        
        for url in detail_urls:
        	yield Request("http://www.mayflower.org.uk/" + url, callback=self.parse_details)
    
    def parse_details(self, response):
	    hxs = HtmlXPathSelector(response)
	    
	    title = hxs.select("//span[@class='EventName2']/text()").extract()[0]
	    date = hxs.select("//p[@class='EventDate']/text()").extract()[0].strip()
	    desc_ps = hxs.select("//p[@class='EventCopy']/node()").extract()
	    desc = "\n".join(desc_ps)
	    
	    return TheatresItem(name=title, date=date, desc=desc, url=response.url)