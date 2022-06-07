import scrapy
import re
from scrapy_splash import SplashRequest


class ProductSpider(scrapy.Spider):
    name = 'product'
    allowed_domains = ['amazon.fr']
    start_urls = ['https://www.amazon.fr/dp/B09M4BFZK7']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse)
    
    def parse(self, response):
        #asin
        asin = response.xpath(".//input[starts-with(@id, 'ASIN')]/@value").get()
        #Nom du produit :
        name = response.xpath('//*[@id="productTitle"]/text()').get().strip().replace(',',' ')
        #Nombre d'évaluation
        nbr_ratings = response.xpath('//*[@data-hook="total-review-count"]/span/text()').get().encode('ascii', 'ignore').decode('UTF-8').strip()
        if nbr_ratings is not None:
            nbr_ratings = re.findall('\d+', nbr_ratings)[0]
        else:
            nbr_ratings = ""
        #Note : Nombre d'étoile sur 5
        pr_stars = response.xpath('//*[@data-hook="average-star-rating"]/span/text()').get()
        if len(pr_stars)!= 0 and pr_stars is not None:
            pr_stars  = re.findall('\d+\,\d+', pr_stars)[0]
        # le lien du produit :
        if asin != None:
            link = 'wwww.amazon.fr/dp/'+asin
        else:
            link=""

        #Caractéristiques produit (les caractéristiques concaténées aves les unes des commentaires)
        table = response.xpath('//table[@class="a-normal a-spacing-micro"]')
        pr_car = table.css("span.a-size-base.a-text-bold::text").getall()
        features = response.xpath('//*[data-hook="cr-summarization-attribute"]/div/div/div[1]/div/span/text()').getall()


        product = {
            'asin' : asin,
            'nom_produit' : name,
            'lien_produit' : link,
            'note' : pr_stars,
            'nb_evaluation': nbr_ratings,
            'features' : pr_car + features
        }
        yield product
        pass