"""
URL configuration for diceit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from. import views
from store import populate_db
from . import rater

urlpatterns = [
    path('', views.home, name='home'),
    path('diventa_artigiano/', views.diventa_artigiano ,name='diventa_artigiano'),
    path('update_reccomendation/', views.update_reccomendation ,name='update_reccomendation'),
    path('store/', include('store.urls')),
    path('hoard/', include('hoard.urls')),
    path('banch/', include('banch.urls')),
    path('admin/', admin.site.urls),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#populate_db.erase_db()
#populate_db.erase_purchase()
#populate_db.create_purchases_db()

#setup per rating
#populate_db.rimuovi_singolo_set("D14")



rater.set_up_reccomendation_file()
#rater.start_update_thread()