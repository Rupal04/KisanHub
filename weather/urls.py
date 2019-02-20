from django.conf.urls import url

from weather.views import fetch_weather_data

urlpatterns = [
                   url(r'^get_weather_data/', fetch_weather_data, name='fetch_weather_data'),
              ]