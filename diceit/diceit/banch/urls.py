from django.urls import path
from . import views


app_name = 'banch'

urlpatterns = [
   path('', views.banch, name='banch'),
   path('add', views.add_set, name='add_set'),
   path('modify', views.banch, name='modify_set'),
]