import datetime
from decimal import Decimal
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from predictor.builder import Builder
from predictor.loader import ExchangeLoader
from predictor.models import Exchange
from predictor.predictor import Predictor
from predictor.serializers import ExchangeMessageSerializer


class ExchangeTestMixin(TestCase):
    def assert_basic_message_is_saved(self):
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


class ExchangeMessageSerializerTestCase(ExchangeTestMixin):
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
        self.assert_basic_message_is_saved()


class ExchangeLoaderTestCase(ExchangeTestMixin):
    def setUp(self):
        self.loader = ExchangeLoader()
        self.response_read = {
            "base": "EUR",
            "date": datetime.date(2018, 10, 5),
            "rates": {
                "CHF": Decimal('1.143300'),
                "GBP": Decimal('0.881650'),
                "USD": Decimal('1.150600'),
            }
        }

    @mock.patch('requests.request')
    def test_read(self, request):
        request.return_value.json.return_value = self.response_read
        today = datetime.date.today()
        # when we call the loader for today
        data = self.loader.read(today)

        # then the API url is called with the right date and
        # the data is returned
        self.assertDictEqual(data, self.response_read)
        request.assert_called_with(
            method='GET',
            url="%s%s" % (self.loader.BASE_API_URL, today.isoformat())
        )
        self.assert_basic_message_is_saved()

    def test_read_period(self):
        with mock.patch.object(ExchangeLoader, 'read',
                               return_value=None) as mock_read:
            # given a start date and an end date 2 days after
            days_to_add = 2
            start_date = datetime.date.today()
            end_date = start_date + datetime.timedelta(days=days_to_add)

            # when we call the read period for this period
            self.loader.read_period(start_date, end_date)

            # then the read method is called 3 times
            mock_read.assert_has_calls([
                mock.call(start_date),
                mock.call(start_date + datetime.timedelta(days=1)),
                mock.call(start_date + datetime.timedelta(days=2))
            ])


class ExchangeViewSetTestCase(APITestCase):
    def test_get_exchanges(self):
        today = datetime.date.today()
        url = "%s?date=%s" % (reverse('exchanges-list'),
                              today.isoformat())
        # create some exchange rows
        builder = Builder()
        exchanges = [
            {
                'base': 'EUR',
                'date': today,
                'goal': 'USD',
                'rate': 1
            },
            {
                'base': 'EUR',
                'date': today,
                'goal': 'CHF',
                'rate': 1
            }
        ]
        for e in exchanges:
            builder.exchange(
                base=e['base'],
                date=e['date'],
                goal=e['goal'],
                rate=e['rate']
            )
        response = self.client.get(url)
        self.assertTrue(len(response.data) == 2)
        item_number = 0
        for item in response.data:
            self.assertEqual(item.get('base'), exchanges[item_number]['base'])
            self.assertEqual(item.get('date'), today.isoformat())
            self.assertEqual(item.get('goal'), exchanges[item_number]['goal'])
            self.assertEqual(Decimal(item.get('rate')),
                             Decimal(exchanges[item_number]['rate']))
            item_number = item_number + 1

    def test_get_prediction(self):
        url = "%s?currency=USD" % reverse('exchanges-predict')
        # predict returns a tuple
        predict_result = (datetime.date(2018, 10, 11), 1.1575, [1.1571],)
        with mock.patch.object(Predictor, 'predict',
                               return_value=predict_result) as mock_predict:
            response = self.client.get(url)
            self.assertTrue(mock_predict.called)
            predicted_dict = {
                'max_date': predict_result[0],
                'last_rate': predict_result[1],
                'prediction': predict_result[2][0],
            }
            self.assertDictEqual(response.data, predicted_dict)


