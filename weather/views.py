from django.shortcuts import render
from django.shortcuts import redirect
from .models import City
from .forms import CityForm
import requests
from collections import defaultdict
import os
from .datetime_functions import get_timezone, get_weekday, get_datetime, get_time


weather_url = os.environ.get("WEATHER_URL")
forecast_url = os.environ.get("FORECAST_URL")


def index(request):
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            form = CityForm

    cities = City.objects.all()

    for city in cities:
        if city.country == None:
            r = requests.get(weather_url.format(city.name, '', city.country)).json()
        else:
            r = requests.get(weather_url.format(city.name, ',', city.country)).json()
        city.temperature = r['main']['temp']
        city.description = r['weather'][0]['description'].capitalize()
        city.icon = r['weather'][0]['icon']
        city.country = r['sys']['country']

    context = {'cities': cities, 'form': form}
    return render(request, 'weather/weather.html', context)


def delete_city(request, pk):
    city = City.objects.get(pk=pk)
    city.delete()
    return redirect('weather:index')


def forecast(request, pk):
    city = City.objects.get(pk=pk)

    if city.country == None:
        r = requests.get(forecast_url.format(city.name, '', city.country)).json()
    else:
        r = requests.get(forecast_url.format(city.name, ',', city.country)).json()

    if city.country == None:
        rn = requests.get(weather_url.format(city.name, '', city.country)).json()
    else:
        rn = requests.get(weather_url.format(city.name, ',', city.country)).json()

    forecasts = range(r['cnt'])

    forecast_dict = defaultdict(list)

    longitude = r['city']['coord']['lon']
    latitude = r['city']['coord']['lat']

    weather_now = {
        'temperature' : rn['main']['temp'],
        'description' : rn['weather'][0]['description'].capitalize(),
        'icon' : rn['weather'][0]['icon'],
        'day' : 'Today',
        'time' : 'Now'
    }

    forecast_dict['Today'].append(weather_now)

    for f in forecasts:
        weather_forecast = {
        'temperature' : r['list'][f]['main']['temp'],
        'description' : r['list'][f]['weather'][0]['description'].capitalize(),
        'icon' : r['list'][f]['weather'][0]['icon'],
        'day' : get_weekday(get_timezone(get_datetime(r['list'][f]['dt']), longitude, latitude)),
        'time' : get_time(get_timezone(get_datetime(r['list'][f]['dt']), longitude, latitude))
        }
        forecast_dict[weather_forecast['day']].append(weather_forecast)

    forecast_data = dict(forecast_dict)

    context = {'city': city, 'forecast_data': forecast_data}

    return render(request, 'weather/forecast.html', context)


def test(request, pk):
    city = City.objects.get(pk=pk)
    test_url = forecast_url.format(city.name, ',', city.country)

    if city.country == None:
        r = requests.get(forecast_url.format(city.name, '', city.country)).json()
    else:
        r = requests.get(forecast_url.format(city.name, ',', city.country)).json()

    my_datetime = get_datetime(r['list'][0]['dt'])

    my_date = my_datetime.date()

    today = datetime.date.today()

    context = {'city': city, 'test_url': test_url, 'my_datetime': my_datetime, 'my_date': my_date, 'today': today}

    return render(request, 'weather/test.html', context)

















