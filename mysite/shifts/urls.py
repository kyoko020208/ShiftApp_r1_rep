from django.urls import path
from . import views


app_name = 'shifts'

urlpatterns=[
    path('calender/', views.Calender.as_view(), name='calender'),
    path('calender/<int:year>-<int:month>/', views.Calender.as_view(), name='calender')
    #path('availability/', views.Availavility.as_view(), name='logout'),
]