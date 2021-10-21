from django.urls import path

from .api_views import *

app_name = 'roommates_api'

urlpatterns = [
    path('geocoding/', SearchGeocodingView.as_view(), name='geocoding'),
    path('housing', HousingView.as_view(), name='housing'),
    path('housing/check', CheckAddressView.as_view(), name='address-check'),
]
