import datetime

from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from predictor.models import Exchange
from predictor.predictor import Predictor
from predictor.serializers import ExchangeSerializer


class ExchangeViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    def list(self, request):
        date = request.query_params.get('date') or datetime.date.today()
        queryset = Exchange.objects.filter(date=date)
        serializer = ExchangeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def predict(self, request):
        currency = request.query_params.get('currency') or 'USD'
        predictor = Predictor()
        max_date, last_rate, prediction = predictor.predict(currency)
        return Response({
            'max_date': max_date,
            'last_rate': last_rate,
            'prediction': prediction[0],
        })


class RetrieveFormView(View):
    template_name = "predictor/retrieve.html"
    form_class = None

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': None})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     pass

        return render(request, self.template_name, {'form': None})


class ForecastFormView(View):
    template_name = "predictor/forecast.html"
    form_class = None

    def get(self, request, *args, **kwargs):
        # form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': None})

    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     pass

        return render(request, self.template_name, {'form': None})
