from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout_then_login
from accounts.views import Index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^accounts/index/$', Index.as_view(), name='account_index'),
]
