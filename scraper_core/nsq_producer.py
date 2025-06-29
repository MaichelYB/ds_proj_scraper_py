# scraper_core/apps.py
from django.apps import AppConfig
import logging
import requests
import json

logger = logging.getLogger(__name__)

class Publisher:
    def __init__(self, nsqd_http_address='http://127.0.0.1:4151'):
        self.nsqd_http_address = nsqd_http_address
    
    def nsq_http_publish(self, topic, message_dict):
        params = {'topic': topic}
        data = json.dumps(message_dict).encode('utf-8')
        try:
            response = requests.post(self.nsqd_http_address + '/pub', params=params, data=data, timeout=3)
            response.raise_for_status()
            print("[NSQ HTTP Producer] Publish success")
        except requests.RequestException as e:
            print("[NSQ HTTP Producer] Publish failed", e)
            raise
    