# Documentation

## install requirements

- Python 3.7 or higher.

## Docker

- install Docker from the website www.docker.com

## installation de splash sur docker

- Pull the image with :
  $ docker pull scrapinghub/splash
- Start container :
  $ docker run -it -p 8050:8050 --rm scrapinghub/splash
- Start splash service in docker container

### install scrapy :

pip install scrapy

### INSTALL external packages into it :

python -m pip install scrapy
start new project
scrapy startproject projet

## Install scrapy-splash

pip install scrapy-splash

## Linking splash with scrapy

### modifier le fichier "settings.py"

- 1- add the splash server to settings.py
  SPLASH_URL = 'http://localhost:8050/'

DOWNLOADER_MIDDLEWARES = {
'scrapy_splash.SplashCookiesMiddleware': 723,
'scrapy_splash.SplashMiddleware': 725,
'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

USER_AGENT = 'project (+http://www.amazone.fr)'

## Lancer le shell interactive

scrapy shell

## récupérer une réponse à partir de l'URL donnée et mettre à jour tous les objets associés en conséquence

fetch('http://localhost:8050/render.html?url=URL')
exemple : fetch('http://localhost:8050/render.html?url=https://www.amazon.fr/product-reviews/B09D8L99FM/')

## Créer un spider

scrapy genspider reviews amazon.fr/

## exécuter un spider et enregistrer la sortie dans un fichier csv

scrapy crawl reviews -o test.csv

scrapy crawl product -o product.csv

## exécuter un spider avec l'envoie d'un argument au spider et enregistrer la sortie dans un fichier csv

scrapy crawl reviews -o ex1_reviews.csv -a asin="B093DY36FF"

<!-- scrapy crawl reviews -o test.csv -a asin="B08Z23JP4W" -->

### send args to spider

scrapy crawl scrapetv -a category=smartphones
