from django.forms import ModelForm, TextInput, ValidationError
from .models import City
import requests


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}

    def clean_name(self):
        name = self.cleaned_data.get('name')
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=08daed9c87b5bb0b625b74e777a6762c'
        r = requests.get(url.format(name)).json()
        if r['cod'] == "404":
            raise ValidationError('Invalid value')
        if r['cod'] == "400":
            raise ValidationError('No value')
        else:
            return name





