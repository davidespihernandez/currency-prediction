import argparse
import datetime

from django.core.management.base import BaseCommand

from predictor.loader import ExchangeLoader


def valid_date(datestr):
    try:
        return datetime.datetime.strptime(datestr, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(datestr)
        raise argparse.ArgumentTypeError(msg)


class Command(BaseCommand):
    help = 'Load exchange info from the API'

    def add_arguments(self, parser):
        parser.add_argument("-s",
                            "--startdate",
                            help="The Start Date - format YYYY-MM-DD",
                            required=False,
                            type=valid_date)
        parser.add_argument("-e",
                            "--enddate",
                            help="The End Date - format YYYY-MM-DD",
                            required=False,
                            type=valid_date)

    def handle(self, *args, **kwargs):
        end_date = kwargs.get('enddate') or datetime.date.today()
        start_date = (kwargs.get('startdate') or
                      end_date - datetime.timedelta(days=90))
        if start_date > end_date:
            raise argparse.ArgumentTypeError("Wrong start or end date")
        loader = ExchangeLoader()
        loader.read_period(start_date=start_date,
                           end_date=end_date,
                           sleep_a_second=True)
