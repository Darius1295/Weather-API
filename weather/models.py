from django.db import models


class City(models.Model):
    name = models.CharField(max_length=20, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=20, blank=True)
    icon = models.FileField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
