import logging

from django.core.management.base import BaseCommand

from wimpy.events.consumers import EventConsumer

__all__ = ['EventConsumer']

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    help = 'Run events consumer'

    def handle(self, *args, **options):
        logger.info('Starting events consumer')
        consumer: EventConsumer = EventConsumer()
        consumer.start()
        logger.info('Events consumer finished')
