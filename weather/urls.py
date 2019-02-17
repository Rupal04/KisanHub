from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^get_weather_data/', fetch_weather_data, name='fetch_weather_data'),
                       )