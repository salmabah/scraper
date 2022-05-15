import scrapy
import re
from scrapy_splash import SplashRequest

script="""
function main(splash, args)
      local url = splash.args.url
      splash:go(url)
      splash:wait(0.5)
      splash:evaljs('$("a[data-hook='cr-translate-these-reviews-link']" ).click();')
      return splash:html()
    end
"""

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['amazon.fr']
    start_urls = ['https://www.amazon.fr/product-reviews/B09M4BFZK7/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, callback=self.parse, args={'lua_source': script})

    def parse(self, response):
        m=['janvier',
            'février',
            'mars',
            'avril',
            'mai',
            'juin',
            'juillet',
            'août',
            'septembre',
            'octobre',
            'novembre',
            'décembre']
        #Nom du produit :
        pr_name = response.xpath('//*[@data-hook="product-link"]/text()').get()
        # le lien du produit :
        pr_link = response.xpath('//*[@data-hook="product-link"]/@href').get()
        
        # scraping reviews
        reviews = response.xpath("//*[@data-hook='review']")

        ## Pour chaque commentaire :
        Date=""
        for elm in reviews:
            Date = elm.xpath('.//*[@data-hook="review-date"]/text()').get()
            li=re.sub('Commenté en ','',Date)
            if li == Date:
                li=re.sub('Commenté au ','',Date)
            li = li.split()
            li.remove("le")
            li[2] = str(m.index(li[2]) + 1)
            stars =  elm.xpath('.//*[@data-hook="review-star-rating"]/span/text()').get()
            if stars == None:
                stars =  elm.xpath('.//*[@data-hook="cmps-review-star-rating"]/span/text()').get()
            if stars is not None:
                stars  = re.findall('\d+\,\d+', stars)[0]
            #titre et contenu du commentaire
            titre = elm.xpath('.//*[@data-hook="review-body"]/span[class="cr-translated-review-content"]/text()').get()
            if titre == None:
                titre = elm.xpath('.//*[@data-hook="review-body"]/span/text()').get()
            body = elm.xpath('.//*[@data-hook="review-body"]/span[class="cr-translated-review-content"]/text()').get()
            if body == None:
                body = elm.xpath('.//*[@data-hook="review-body"]/span/text()').get()
            review = {
            #asin
            'asin' : 'B09M4BFZK7',
            #Nombre d'étoiles :
            'rv_stars_rating' : stars,
            #Titre
            'rv_titre' : titre,
            #Date et pays
            'rv_date' : li[1]+'/'+li[2]+'/'+li[3],
            'rv_pays' : li[0],
            #Achat vérifié
            'rv_achat' : elm.xpath('.//*[@data-hook="avp-badge"]/text()').get(),
            #Contenu du commentaire
            'rv_body' : body,
            #Nb personnes qu'ont trouvé le commentaire utile
            'rv_utile' : elm.xpath('.//*[@data-hook="helpful-vote-statement"]/text()').get(),
            #Lien du commentaire
            'rv_lien' : elm.xpath('.//*[@data-hook="review-title"]/@href').get()
            }
            yield review
        
        next_page = response.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a//@href').get()
        if next_page is not None:
            yield response.follow('www.amazon.fr'+next_page, callback=self.parse)
        
        pass

