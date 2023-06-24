from django.urls import path
from . import views


app_name = 'hoard'

urlpatterns = [
   path('', views.hoard, name='hoard'),
   path('show_hoard/<str:user>/', views.show_hoard, name='show_hoard'),
   path('explore_hoards/', views.explore_hoards, name='explore_hoards'),

]