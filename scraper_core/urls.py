from django.urls import path
from django.http import HttpResponse

from scraper_core.views import Scraper

def health_check(request):
    return HttpResponse("Server is running", status=200)

def news_scraper(request):
    newScraper = Scraper(request)
    return newScraper.scraper_news()

def stock_scraper(request):
    return HttpResponse("Server is running", status=200)

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('news-scrape/', news_scraper, name='news-scraper'),
]