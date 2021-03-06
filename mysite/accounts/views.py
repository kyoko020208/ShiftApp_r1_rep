from __future__ import unicode_literals
from django.views.generic import View
from .forms import ManagerStatusForm, SignUpForm, LoginForm
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ManagerStatusView(View):
    def get_context_data(self, request, **kwargs):
        return render(request, 'accounts/ManagerStatus.html')

    def post(self, request, *args, **kwargs):
        form = ManagerStatusForm()
        is_manager = form.cleaned_data['is_manager']
        context = {
            'is_manager': is_manager,
        }
        return redirect('accounts:signup', context)


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        """create method for get request"""
        #set SignUpForm as form
        form = SignUpForm()
        #return SignUp page with empty form
        return render(request, 'accounts/signup.html', {'form': form})

    def post(self, request):
        """create method for post request"""
        #set request form as new form
        form = SignUpForm(request.POST)
        #validation; if the form is invalid, return empty form again
        if not form.is_valid():
            return render(request, 'accounts/signup.html', {'form': form})

        #save form info into user database
        user_info_save = form.save(commit=True)
        user_info_save.set_password(form.cleaned_data['password'])
        user_info_save.save()

        # #login; save the user data and update the database
        # auth_login(request, user_info_save)

        #redirect to shift index
        return redirect('shifts:index')


class LoginView(View):
    """create method for get request"""
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form':form})

    """create method for post request"""
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/login.html', {'form':form})

        #get the user info from the form
        login_user = form.get_login_user()

        auth_login(request, login_user)
        return redirect(reverse('shifts:index'))

class LogoutView(LoginRequiredMixin, View):
    """create method for get request"""
    def get(self, request, *args, **kwargs):
        #if the user was authenticated, logout and clear the session
        if request.user.is_authenticated:
            auth_logout(request)

        #redirect to login page
        return redirect(reverse('accounts:login'))

