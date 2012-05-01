from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from theatres.items import *


class TurnerSimsSpider(BaseSpider):
    name = "turnersims"
    allowed_domains = ["turnersims.co.uk"]
    start_urls = ["http://www.turnersims.co.uk/upcoming-events/?page=1"]

    location = "Turner Sims Concert Hall"
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        detail_urls = hxs.select("//h3/a/@href").extract()
        
        for url in detail_urls:
        	yield Request("http://www.turnersims.co.uk" + url, callback=self.parse_details)
        	
        next_url = hxs.select("//a[@class='next']/@href").extract()[0]
        yield Request("http://www.turnersims.co.uk" + next_url, callback=self.parse)
    
    def parse_details(self, response):
    	hxs = HtmlXPathSelector(response)
    	title = hxs.select("//div[@id='contentHeader']/h1/text()").extract()[0]
    	#title += " : " + hxs.select("//div[@id='contentHeader']/h2/text()").extract()[0]
    	date = hxs.select("//span[@class='date']/text()").extract()[0].strip()
    	desc_ps = hxs.select("//div[@id='colB']/p[not(@class)]/node()").extract()
    	desc = "\n".join(desc_ps)
    	desc = self.remove_html(desc)
    	
    	return TheatresItem(name=title, date=date, desc=desc, url=response.url)
    
    def remove_html(self, string):
    	import re
    	p = re.compile(r'<.*?>')
    	return p.sub('', string)