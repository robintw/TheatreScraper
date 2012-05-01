from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from theatres.items import *


class NuffieldSpider(BaseSpider):
    name = "nuffield"
    allowed_domains = ["nuffieldtheatre.co.uk"]
    start_urls = ["http://www.nuffieldtheatre.co.uk/events/category/C84/"]

    location = "Nuffield Theatre"
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        detail_urls = hxs.select("//h2/a/@href").extract()
        
        for url in detail_urls:
        	yield Request(url, callback=self.parse_details)
        	
        next_url = hxs.select("//p[@class='paginate_links']/a[text()='Next Page']/@href").extract()[0]
        yield Request(next_url, callback=self.parse)
    
    def parse_details(self, response):
	    hxs = HtmlXPathSelector(response)
	    
	    title = hxs.select("//h1/text()").extract()[0]
	    date = hxs.select('//p[@class="date"]/text()').extract()[0].strip()
	    desc_ps = hxs.select("//div[@id='main_content' and @class='col six float single']/p/text()").extract()
	    desc = "\n".join(desc_ps)
	    
	    return TheatresItem(name=title, date=date, desc=desc, url=response.url)