"""currency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from predictor.views import ExchangeViewSet, RetrieveFormView, ForecastFormView

router = DefaultRouter()
router.register(r'exchanges/?', ExchangeViewSet, base_name='exchanges')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('retrieve/', RetrieveFormView.as_view(), name="retrieve"),
    url('forecast/', ForecastFormView.as_view(), name="forecast")
]

urlpatterns += router.urls
