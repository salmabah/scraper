# Documentation

## Set up the envirement in Windows

# Docker

- install Docker from the website www.docker.com

# installation de splash sur docker

- Pull the image with :
  $ docker pull scrapinghub/splash
- Start container :
  $ docker run -it -p 8050:8050 --rm scrapinghub/splash
- Start splash service in docker container

### set up the virtual envirement :

- move to the folder where the project should be in, then run these comands
  > > python -m venv venv
  > > venv\Scripts\Activate

### install external dependencies :

pip install scrapy

### INSTALL external packages into it :

python -m pip install scrapy
start new project
scrapy startproject projet

# Install scrapy-splash

pip install scrapy-splash

# Linking splash with scrapy

<!-- modifier le fichier settings.py -->

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

-

## Lancer le shell interactive

shell scrapy URL

## Créer un spider

scrapy genspider reviews amazon.fr/

scrapy crawl reviews -o test.csv

<!-- send args to spider -->

scrapy crawl scrapetv -a category=smartphones

fetch('http://localhost:8050/render.html?url=https://www.amazon.fr/product-reviews/B09D8L99FM/')
