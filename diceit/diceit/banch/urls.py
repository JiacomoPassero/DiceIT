from django.urls import path
from . import views


app_name = 'banch'

urlpatterns = [
   path('', views.banch, name='banch'),
   path('add', views.CreateDiceView.as_view(), name='add_set'),
   path('modify', views.modify_set, name='modify_set'),
]