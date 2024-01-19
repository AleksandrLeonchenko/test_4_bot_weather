from django.db import models


class WeatherData(models.Model):
    """
    Модель данных о погоде в городах
    """
    city = models.CharField(max_length=255)
    temperature = models.FloatField()
    pressure = models.FloatField()
    wind_speed = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name = 'Данные о погоде'
        verbose_name_plural = 'Данные о погоде'
        ordering = ['pk']
