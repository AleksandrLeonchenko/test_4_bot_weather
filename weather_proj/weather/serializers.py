from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    """
    Сериализатор для модели погоды.

    """
    temperature = serializers.FloatField(default=None)
    pressure = serializers.FloatField(default=None)
    wind_speed = serializers.FloatField(default=None)
