import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import WeatherSerializer
from .service import get_weather_data
from typing import Any, Dict


class WeatherAPIView(APIView):
    """
    API-представление для получения данных о погоде.

    **Параметры запроса:**
    - `city` (строка): Название города, для которого запрашиваются данные о погоде.

    **Пример запроса:**
    ```
    /api/weather/?city=Москва
    ```

    **Пример ответа:**
    ```json
    {
        "temperature": 20,
        "pressure": 760,
        "wind_speed": 5
    }
    ```

    **Возможные ошибки:**
    - `400 Bad Request`: Если параметр `city` не указан.
    """
    def get(self, request, *args, **kwargs) -> Response:
        """
        Обработчик GET-запроса.

        :param request: Объект запроса.
        :param args: Дополнительные аргументы.
        :param kwargs: Дополнительные именованные аргументы.
        :return: Ответ с данными о погоде или сообщение об ошибке.
        """
        city_name = self.request.GET.get('city', '').lower()

        if not city_name:
            return Response({'error': 'Параметр <город> не указан.'}, status=status.HTTP_400_BAD_REQUEST)

        weather_data = get_weather_data(city_name)
        serializer = WeatherSerializer(weather_data)

        return Response(serializer.data)

