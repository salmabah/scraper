import scrapy
import re
from scrapy_splash import SplashRequest
from scrapy.utils.python import to_native_str

# script="""
# function main(splash, args)
#       local url = splash.args.url
#       splash:go(url)
#       splash:wait(0.5)
#       splash:evaljs('$("*[data-hook='cr-translate-these-reviews-link']" ).click();')
#       return splash:html()
#     end
# """

def format_date(d, m, y):
    d, m = int(d), int(m)
    if m < 10:
        m = '0'+str(m)
    if d < 10:
        d = '0'+str(d)
    d,m = str(d), str(m)
    date = d+"/"+m+"/"+str(y)
    return (date)

class ReviewsSpider(scrapy.Spider):
    id = 0
    name = 'reviews'
    allowed_domains = ['amazon.fr']
    start_urls = ['https://www.amazon.fr/product-reviews/B07ZHJFH4W']
    asin = ''

    def __init__(self, asin=None, *args, **kwargs):
        super(ReviewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f'https://www.amazon.fr/product-reviews/{asin}']
        self.asin = {asin}

    def start_requests(self):
        for url in self.start_urls:
            url = to_native_str(url)
            yield SplashRequest(url, callback=self.parse)

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
            #id
            ReviewsSpider.id += 1

            Date = elm.xpath('.//*[@data-hook="review-date"]/text()').get()
            
            if 'aux' in Date:
                li = re.sub('Commenté aux ','',Date)
            elif 'au' in Date:
                li = re.sub('Commenté au ','',Date)
            elif 'en' in Date:
                li=re.sub('Commenté en ','',Date)
            
            li = li.split()
            li.remove("le")
            li[2] = str(m.index(li[2]) + 1)
            # formater la date sous la forme dd/mm/yyyy
            date = format_date(li[1],li[2],li[3])
            stars =  elm.xpath('.//*[@data-hook="review-star-rating"]/span/text()').get()
            if stars == None:
                stars =  elm.xpath('.//*[@data-hook="cmps-review-star-rating"]/span/text()').get()
            if stars is not None:
                stars = re.findall('\d+\,\d+', stars)[0]
                stars = stars.strip('"')

            #titre et contenu du commentaire
            # titre = elm.xpath('.//*[@data-hook="review-title"]/span[class="cr-translated-review-content"]/text()').get()
            # if titre == None:
            titre = elm.xpath('.//*[@data-hook="review-title"]/span/text()').get()
            # body = elm.xpath('.//*[@data-hook="review-body"]/span[class="cr-translated-review-content"]/text()').getall()
            # if body == None:
            body = elm.xpath('.//*[@data-hook="review-body"]/span/text()').getall()
            body = ' '.join([str(item) for item in body])
            # if body is not None:
            #     body = body.strip('"')
            if titre is not None:
                titre = titre.strip('"')
            
            review = {
                'id': ReviewsSpider.id,
                #asin
                'asin' : str(self.asin).strip("{}'"),
                #Nombre d'étoiles :
                'rv_stars_rating' : stars,
                #Titre
                'rv_titre' : titre,
                #Date et pays
                'rv_date' : date,
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
        # if next_page 
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        
        pass
