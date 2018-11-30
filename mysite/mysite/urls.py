from django.contrib import admin
from django.urls import include, path

#from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('login/index', views.index.asView, name='index'),
    path('accounts/', include('accounts.urls')),
]
