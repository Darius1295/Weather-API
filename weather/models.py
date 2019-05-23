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


class BucketManager(models.Manager):
    def new_or_get(self, request):
        bucket_id = request.session.get("bucket_id", None)
        request.session.save()
        qs = self.get_queryset().filter(id=bucket_id)
        if qs.count() == 1:
            new_obj = False
            bucket_obj = qs.first()
            bucket_obj.save()
        else:
            bucket_obj = Bucket.objects.new()
            new_obj = True
            request.session['bucket_id'] = bucket_obj.id
        return bucket_obj, new_obj

    def new(self):
        return self.model.objects.create()


class Bucket(models.Model):
    cities = models.ManyToManyField(City, blank=True)

    objects = BucketManager()

    def __str__(self):
        return str(self.id)

