from django.urls import path
from .api import WeatherAPIView
from .views import start_bot, stop_bot


urlpatterns = [
    path('weather', WeatherAPIView.as_view(), name='weather_api'),
    path('bot_start/', start_bot, name='start_bot'),
    path('bot_stop/', stop_bot, name='stop_bot'),
]