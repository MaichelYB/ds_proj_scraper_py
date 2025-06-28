from django.apps import AppConfig
from django.conf import settings  # <-- THIS WAS MISSING
from .services.nsq_producer import producer
import atexit
import time
import logging

logger = logging.getLogger(__name__)


class ScrapeNewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scrape_news'
            
