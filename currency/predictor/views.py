import datetime

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from predictor.models import Exchange
from predictor.serializers import ExchangeSerializer


class ExchangeViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    def list(self, request):
        date = request.query_params.get('date') or datetime.date.today()
        queryset = Exchange.objects.filter(date=date)
        serializer = ExchangeSerializer(queryset, many=True)
        return Response(serializer.data)
