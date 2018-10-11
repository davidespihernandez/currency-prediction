import logging
import time
import requests, logging

from datetime import timedelta

from predictor.models import Exchange
from predictor.serializers import ExchangeMessageSerializer


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


logger = logging.getLogger(__name__)


class ExchangeLoader:
    """
    Reads the exchange info from the API
    and loads it into the database
    """
    BASE_API_URL = 'https://api.exchangeratesapi.io/'

    def read(self, date):
        """
        Reads data for a specific date and loads that data into the database
        :param date: Date to load
        :returns The serializer save() results
        """
        response = requests.request(
            method='GET',
            url="%s%s" % (self.BASE_API_URL, date.isoformat())
        )
        serializer = ExchangeMessageSerializer(data=response.json())
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def read_period(self, start_date, end_date, sleep_a_second=False):
        """
        Loads a period between 2 dates
        :param sleep_a_second: True to sleep a second between calls
        :param start_date: Start date
        :param end_date: End date
        """
        logger.info("Load from %s to %s" % (start_date, end_date, ))
        for single_date in date_range(start_date, end_date):
            if self.date_is_already_loaded(single_date):
                logger.info("Skipping %s as is already loaded" % single_date)
                continue
            self.read(single_date)
            if sleep_a_second:
                logger.info("Loaded %s" % str(single_date))
                time.sleep(1)

    @staticmethod
    def date_is_already_loaded(date):
        return Exchange.objects.filter(date=date).exists()
