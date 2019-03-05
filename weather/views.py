from django.shortcuts import render
from django.shortcuts import redirect
from .models import City
from .forms import CityForm
import requests


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
            r = requests.get(url.format(city.name,'', city.country)).json()
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
