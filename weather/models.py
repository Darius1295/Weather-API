from django.db import models
from django_countries.fields import CountryField


class City(models.Model):
    name = models.CharField(max_length=20, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=20, blank=True)
    icon = models.FileField(blank=True)
    country = CountryField(blank=True, blank_label='select country (optional)')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
