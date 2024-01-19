from django.contrib import admin
from .models import WeatherData
from typing import List


class WeatherDataAdmin(admin.ModelAdmin):
    list_display: List[str] = [
        'id',
        'city',
        'temperature',
        'pressure',
        'wind_speed',
        'last_updated',
    ]
    list_display_links: List[str] = [
        'id',
        'city',
        'temperature',
        'pressure',
        'wind_speed',
        'last_updated',
    ]


admin.site.register(WeatherData, WeatherDataAdmin)

admin.site.site_title = 'Админ-панель weather_proj'
admin.site.site_header = 'Админ-панель weather_proj'
