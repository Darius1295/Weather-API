import requests
from django.shortcuts import render
from .models import City


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=08daed9c87b5bb0b625b74e777a6762c'

    weather_list = []
    cities = City.objects.all()

    for city in cities:
        r = requests.get(url.format(city)).json()
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        print(city_weather)
        weather_list.append(city_weather)

    print(weather_list)

    context = {'weather_list': weather_list}

    return render(request, 'weather/weather.html', context)

