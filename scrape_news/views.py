from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from scrape_news.nsq_producer import Publisher

# Create your views here.
class ScraperNews:
    def __init__(self, url):
        self.url = url

    def extract_time_ago(self,text):
        """
        Extracts (quantity, unit) from strings like:
        'Yahoo Finance • 16 hours ago'
        'Yahoo Finance • 1 day ago'
        'Yahoo Finance • 5 minutes ago'

        Returns:
            (16, 'hours')
            (1, 'day')
            (5, 'minutes')
        or (None, None) if not found.
        """
        match = re.search(r'(\d+)\s+(minute|minutes|hour|hours|day|days)\s+ago', text)
        if match:
            quantity = int(match.group(1))
            unit = match.group(2)
            return [quantity, unit]
        else:
            return [0, '']

    def scrape_news(self):
        options = Options()
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        options.add_argument("--headless=new")  # use "--headless" if older Chrome
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")  # ensure consistent rendering

        service = Service("/opt/homebrew/bin/chromedriver")  # replace with your chromedriver path
        driver = webdriver.Chrome(service=service, options=options)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        # driver = webdriver.Chrome(options=options)  # Selenium will auto-download chromedriver
        # driver = webdriver.Chrome()
        driver.get(self.url)
        dataList = driver.find_elements(By.CLASS_NAME, "stream-item.story-item")
        for data in dataList:
            try:
                story = {}
                a_tag = data.find_element(By.TAG_NAME, "a")
                story['link'] = a_tag.get_attribute("href")
                story['title'] = data.find_element(By.CSS_SELECTOR, "h3.clamp").text
                story['content'] = data.find_element(By.CSS_SELECTOR, "p.clamp").text
                story['date'] = self.extract_time_ago(data.find_element(By.CLASS_NAME, "publishing").text)
                # publish the story to nsq
                publisher = Publisher()
                publisher.nsq_http_publish('news_scrapper', story)
            except:
                print("No link found in this item.")
        driver.quit()