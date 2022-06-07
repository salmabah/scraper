import scrapy
from scrapy_splash import SplashRequest


class ScrapetvSpider(scrapy.Spider):
    name = 'scrapetv'
    allowed_domains = ['amazon.fr']
    start_urls = [f'https://www.amazon.fr/s?k=téléviseurs']
    category = ''
    def __init__(self, category=None, *args, **kwargs):
        super(ScrapetvSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.amazon.fr/s?k={category}']
        self.category = {category}

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse)
    
    def parse(self, response):
        x=response.xpath('//*[@data-asin]/@data-asin').getall()
        asin_list = list(filter(None, x))

        for elm in asin_list:
            ctg={
                'asin' : elm,
                'catégorie' : str(self.category).strip("{}'")
            }
            yield ctg
        # next_page = response.xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[55]/div/div/span/a[3]/@href').get()
        next_page = response.xpath('//*[@class="s-pagination-strip"]/a[last()]/@href').get()
        if next_page is not None:
            yield response.follow('www.amazon.fr'+next_page, callback=self.parse)
        pass
