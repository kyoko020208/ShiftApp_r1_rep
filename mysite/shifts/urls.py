from django.urls import path
from . import views


app_name = 'shifts'

urlpatterns=[
    path('index/', views.HomeView.as_view(), name='index'),
    path('index/shiftsadd/', views.ShiftAddView.as_view(), name='shiftsadd')
    #path('availability/', views.Availavility.as_view(), name='logout'),
]