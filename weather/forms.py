from django.forms import ModelForm, TextInput, ValidationError
from .models import City
import requests
import os

weather_url = os.environ.get("WEATHER_URL")
forecast_url = os.environ.get("FORECAST_URL")


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'country']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        country = cleaned_data.get('country')
        print("Cleaned name: " + str(name))
        print("Cleaned country: " + str(country))
        if country == '':
            url = weather_url.format(name, '', '')
            print(url)
            r = requests.get(url).json()
        else:
            url = weather_url.format(name, ',', country)
            print(url)
            r = requests.get(url).json()
        print(r)
        if r['cod'] == "404":
            print('City not found ValidationError')
            raise ValidationError('City not found. Please check if spelling or country selected is correct.')
        if r['cod'] == "400":
            print('No city entered ValidationError')
            raise ValidationError('Please enter a city name.')




