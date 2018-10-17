import datetime
import json

from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from predictor.forms import RetrieveForm, ForecastForm
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
    form_class = RetrieveForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = "No data available"
        if form.is_valid():
            queryset = Exchange.objects.filter(date=form.cleaned_data['date'])
            serializer = ExchangeSerializer(queryset, many=True)
            data = json.dumps(serializer.data, indent=4)

        return render(
            request,
            self.template_name,
            {'form': form, 'data': data}
        )


class ForecastFormView(View):
    template_name = "predictor/forecast.html"
    form_class = ForecastForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={"currency": "USD"})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        data = "No data available"
        if form.is_valid():
            currency = form.cleaned_data.get('currency')
            predictor = Predictor()
            max_date, last_rate, prediction = predictor.predict(currency)
            data = json.dumps({
                'max_date': max_date.isoformat(),
                'last_rate': str(last_rate),
                'prediction': str(prediction[0]),
            }, indent=4)

        return render(
            request,
            self.template_name,
            {'form': form, 'data': data}
        )
