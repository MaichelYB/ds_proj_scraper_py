import json
from scrape_news.views import ScraperNews

def handler(message):
    try:
        data = json.loads(message.body)
        print("[NSQ] Received data:", data)
        url = data['url']
        category = data['category']
        newsScraper = ScraperNews(url)
        newsScraper.scrape_news()

        return True  # message finished
    except Exception as e:
        print("[NSQ] Error processing message:", e)
        return False  # requeue or finish based on your needs