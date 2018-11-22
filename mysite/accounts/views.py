from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.views.generic import View
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class Index(View):
    #method_decorator(login_required)
    def get(selfseld, request):
        return render(request, 'accounts/index.html')
