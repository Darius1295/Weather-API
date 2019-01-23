import requests
from django.shortcuts import render


def index(request):
    url = 'http://samples.openweathermap.org/data/2.5/find?q={}&units=metric&appid=b6907d289e10d714a6e88b30761fae22'

    city = 'London'
    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['list'][0]['main']['temp'],
        'description': r['list'][0]['weather'][0]['description'],
        'icon': r['list'][0]['weather'][0]['icon']
    }

    print(city_weather)

    context = {'city_weather': city_weather}

    return render(request, 'weather/weather.html', context)

