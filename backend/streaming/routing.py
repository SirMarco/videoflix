# routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'wss/conversion-status/', consumers.ConversionStatusConsumer.as_asgi()),
]
