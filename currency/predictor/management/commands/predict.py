import logging

from django.core.management.base import BaseCommand

from predictor.predictor import Predictor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Predicts next value for a currency based on the loaded data.' \
           ' Base es EUR.'

    def add_arguments(self, parser):
        parser.add_argument("-c",
                            "--currency",
                            help="The currency to predict. Default is USD",
                            required=False,
                            type=str)

    def handle(self, *args, **kwargs):
        currency = kwargs.get('currency') or 'USD'
        predictor = Predictor()
        max_date, last_rate, prediction = predictor.predict(currency)
        logger.info(
            "Last date stored: %s, rate was %s - predicted value: %s" % (
                max_date.isoformat(),
                last_rate,
                prediction[0])
        )
