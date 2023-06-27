from django.urls import path
from . import views


app_name = 'banch'

urlpatterns = [
   path('', views.banch, name='banch'),
   path('add', views.CreateDiceView.as_view(), name='add_set'),
   path('view_sets', views.view_sets, name='view_sets'),
   path('modify_set/<str:pk>/update/', views.UpdateDiceView.as_view(), name='modify_set'),
]