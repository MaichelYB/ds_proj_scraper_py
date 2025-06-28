from django.urls import path
from django.http import HttpResponse

from scrape_news.views import ScraperNews

def health_check(request):
    return HttpResponse("Server is running", status=200)

def news_scraper(request):
    newScraper = ScraperNews()
    newScraper.scrape_news(request)
    return HttpResponse("Server is running", status=200)

urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('news-scrape/', news_scraper, name='news-scraper'),
]
