from django.core.management.base import BaseCommand
import nsq
from scrape_news.nsq_consumer import handler

class Command(BaseCommand):
    help = "Run NSQ consumer"

    def handle(self, *args, **options):
        r = nsq.Reader(
            message_handler=handler,
            topic='news_core',
            channel='py_news_core',
            nsqd_tcp_addresses=['127.0.0.1:4150'],  # point to your nsqd
        )
        nsq.run()