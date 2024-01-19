import os
import requests
from dotenv import load_dotenv
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from geopy.geocoders import Nominatim
from typing import Dict, Union

from .models import WeatherData

load_dotenv()


def get_weather_data(city_name: str) -> Union[Dict[str, Union[float, str]], None]:
    """
    Получает данные о погоде для указанного города.

    :param city_name: Название города.
    :return: Словарь с данными о погоде или None в случае ошибки.
    """
    weather_data = WeatherData.objects.filter(city=city_name).first()

    if weather_data is None or (
            weather_data and (timezone.now() - weather_data.last_updated > timedelta(minutes=5))):
        api_key = os.getenv("YANDEX_API_KEY")
        lat, lon = get_coordinates(city_name)

        if lat is None or lon is None:
            return None
        url = f'https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}'
        headers = {'X-Yandex-API-Key': api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            temperature = data['fact']['temp']
            pressure = data['fact']['pressure_mm']
            wind_speed = data['fact']['wind_speed']

            if not weather_data:
                weather_data = WeatherData(city=city_name, temperature=temperature, pressure=pressure,
                                           wind_speed=wind_speed)
            else:
                weather_data.temperature = temperature
                weather_data.pressure = pressure
                weather_data.wind_speed = wind_speed
            weather_data.save()

            return {
                'temperature': temperature,
                'pressure': pressure,
                'wind_speed': wind_speed,
            }

    elif weather_data:
        return {
            'temperature': weather_data.temperature,
            'pressure': weather_data.pressure,
            'wind_speed': weather_data.wind_speed
        }

    else:
        return {'error': 'Произошла ошибка при запросе.'}


def get_coordinates(city_name: str) -> Union:
    """
    Получает координаты для указанного города.

    :param city_name: Название города.
    :return: Словарь с координатами или None в случае ошибки.
    """
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None
