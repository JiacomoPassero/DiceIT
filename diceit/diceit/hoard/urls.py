from django.urls import path
from . import views


app_name = 'hoard'

urlpatterns = [
   path('', views.hoard, name='hoard'),
]