from django.shortcuts import render
from django.shortcuts import redirect
from .models import City
from .forms import CityForm
import requests
import datetime
import calendar


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}{}{}&units=metric&appid=08daed9c87b5bb0b625b74e777a6762c'

    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            form = CityForm

    cities = City.objects.all()

    for city in cities:
        if city.country == None:
            r = requests.get(url.format(city.name, '', city.country)).json()
        else:
            r = requests.get(url.format(city.name, ',', city.country)).json()
        city.temperature = r['main']['temp']
        city.description = r['weather'][0]['description'].capitalize()
        city.icon = r['weather'][0]['icon']
        city.country = r['sys']['country']

    print(cities)

    context = {'cities': cities, 'form': form}
    return render(request, 'weather/weather.html', context)


def delete_city(request, pk):
    city = City.objects.get(pk=pk)
    city.delete()
    return redirect('weather:index')


def get_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def get_weekday(date):
    if date.strftime('%Y-%m-%d') == datetime.date.today():
        return 'Today'
    else:
        return calendar.day_name[date.weekday()]


def get_time(date):
    return date.time().strftime('%H:%M')


def forecast(request, pk):
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}{}{}&units=metric&appid=08daed9c87b5bb0b625b74e777a6762c'

    city = City.objects.get(pk=pk)

    if city.country == None:
        r = requests.get(url.format(city.name, '', city.country)).json()
    else:
        r = requests.get(url.format(city.name, ',', city.country)).json()

    forecasts = range(39)

    forecast_data = []

    for f in forecasts:
        weather_forecast = {
        'temperature' : r['list'][f]['main']['temp'],
        'description' : r['list'][f]['weather'][0]['description'].capitalize(),
        'icon' : r['list'][f]['weather'][0]['icon'],
        'day' : get_weekday(get_date(r['list'][f]['dt'])),
        'time' : get_time(get_date(r['list'][f]['dt']))
        }
        forecast_data.append(weather_forecast)

    context = {'city': city, 'forecast_data': forecast_data}

    return render(request, 'weather/forecast.html', context)


def test(request, pk):
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}{}{}&units=metric&appid=08daed9c87b5bb0b625b74e777a6762c'

    city = City.objects.get(pk=pk)
    test_url = url.format(city.name, ',', city.country)

    if city.country == None:
        r = requests.get(url.format(city.name, '', city.country)).json()
    else:
        r = requests.get(url.format(city.name, ',', city.country)).json()

    date = get_date(r['list'][0]['dt'])

    s_date = date.strftime('%Y-%m-%d')

    today = datetime.date.today()

    context = {'city': city, 'test_url': test_url, 'date': date, 's_date': s_date, 'today': today}

    return render(request, 'weather/test.html', context)

















