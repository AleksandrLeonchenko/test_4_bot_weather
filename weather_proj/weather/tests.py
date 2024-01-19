from django.test import TestCase
from unittest.mock import patch
from typing import Any

from .service import get_coordinates, get_weather_data
from .bot import get_weather


class UtilsTests(TestCase):
    def test_get_coordinates_valid_city(self) -> None:
        """
        Тест-кейс для функции get_coordinates с корректным названием города.
        """
        lat, lon = get_coordinates("Москва")
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)

    def test_get_coordinates_invalid_city(self) -> None:
        """
        Тест-кейс для функции get_coordinates с некорректным названием города.
        """
        lat, lon = get_coordinates("Ку112")
        self.assertIsNone(lat)
        self.assertIsNone(lon)

    def test_get_weather_data_valid_city(self) -> None:
        """
        Тест-кейс для функции get_weather_data с корректным названием города.
        """
        data = get_weather_data("Москва")
        self.assertIsNotNone(data)
        self.assertIn('temperature', data)
        self.assertIn('pressure', data)
        self.assertIn('wind_speed', data)

    def test_get_weather_data_invalid_city(self) -> None:
        """
        Тест-кейс для функции get_weather_data с некорректным названием города.
        """
        data = get_weather_data("Ку112")
        self.assertIsNotNone(data)
        self.assertIn('error', data)


class BotTestCase(TestCase):
    @patch('.bot.get_weather_data')
    def test_get_weather(self, mock_get_weather_data: Any) -> None:
        """
        Тест-кейс для функции get_weather.
        """
        mock_get_weather_data.return_value = {
            'temperature': 20, 'pressure': 760, 'wind_speed': 5
        }

        response = get_weather('Москва')

        expected_response = "В городе test_city сейчас температура 20°C, давление 760 мм.рт.ст, скорость ветра 5 м/с."
        self.assertEqual(response, expected_response)
