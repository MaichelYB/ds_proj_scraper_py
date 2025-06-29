from django.shortcuts import render
from scraper_core.nsq_producer import Publisher
from django.http import JsonResponse
import requests

# Create your views here.
class Scraper:
    def __init__(self, request):
        self.request = request
        self.optionCategories = [
            'latest',
            'stock-market-news',
            'yahoo-finance-originals',
            'economic-news',
            'tech',
            'housing-market',
            'mergers-ipos',
            'electric-vehicles'
        ]
        self.newsURL = "https://finance.yahoo.com/topic/"
        self.newsTopic = "news_core"
        self.stockTopic = "stock_core"

    def scraper_news(self):
        for category in self.optionCategories:
            url = self.newsURL + category
            payload = {
                "url": url,
                "category": category
            }
            publiser = Publisher()
            try:
                publiser.nsq_http_publish(self.newsTopic, payload)
            except requests.RequestException as e:
                print("[Caller] Failed to publish to NSQ:", e)
                return JsonResponse({"status": "error", "message": "Failed to publish to NSQ"}, status=500)
        return JsonResponse({"status": "success", "message": "Data published to NSQ"})
            