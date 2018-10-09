import datetime
from decimal import Decimal

from django.test import TestCase

from predictor.models import Exchange
from predictor.serializers import ExchangeMessageSerializer


class ExchangeMessageSerializerTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.message = {
            "base": "EUR",
            "date": "2018-10-05",
            "rates": {
                "GBP": 0.88165,
                "USD": 1.1506,
                "CHF": 1.1433
            }
        }
        self.serialized = {
            "base": "EUR",
            "date": datetime.date(2018, 10, 5),
            "rates": {
                "CHF": Decimal('1.143300'),
                "GBP": Decimal('0.881650'),
                "USD": Decimal('1.150600'),
            }
        }

    def test_message_is_deserialized(self):
        serializer = ExchangeMessageSerializer(data=self.message)
        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(self.serialized,
                             serializer.validated_data)

    def test_message_is_saved(self):
        serializer = ExchangeMessageSerializer(data=self.message)
        serializer.is_valid()
        serializer.save()
        self.assertEqual(3,
                         Exchange.objects.count())
        self.assertTrue(
            Exchange.objects.filter(
                base='EUR',
                date=datetime.date(2018, 10, 5),
                goal='CHF',
                rate=Decimal('1.143300')
            ).exists()
        )
        self.assertTrue(
            Exchange.objects.filter(
                base='EUR',
                date=datetime.date(2018, 10, 5),
                goal='GBP',
                rate=Decimal('0.881650')
            ).exists()
        )
        self.assertTrue(
            Exchange.objects.filter(
                base='EUR',
                date=datetime.date(2018, 10, 5),
                goal='USD',
                rate=Decimal('1.150600')
            ).exists()
        )
