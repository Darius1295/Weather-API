from django.urls import path
from . import views


app_name = 'weather'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/delete', views.delete_city, name='delete-city'),
]
