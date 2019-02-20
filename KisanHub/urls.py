from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/weather/', include("weather.urls")),
]
