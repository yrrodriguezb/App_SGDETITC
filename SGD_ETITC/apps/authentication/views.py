# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordChangeView, 
    PasswordResetView, 
    PasswordResetConfirmView,
    PasswordResetDoneView
)
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import FormView, RedirectView, CreateView


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "authentication/login.html"
    success_url =  reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class PasswdChangeView(PasswordChangeView):
    template_name = "authentication/password_change.html"
    success_url = reverse_lazy("password_change")

    def get_success_url(self):
        self.success_url = str(self.success_url + "?success")
        return super(PasswdChangeView, self).get_success_url()


class PasswdResetView(PasswordResetView):
    template_name = "authentication/password_reset.html"
    success_url = reverse_lazy('password_reset')

    def get_success_url(self):
        self.success_url = str(self.success_url + "?success")
        return super(PasswdResetView, self).get_success_url()


class PasswdResetConfirmView(PasswordResetConfirmView):
    template_name = "authentication/password_reset_confirm.html"
    success_url = reverse_lazy('password_reset_complete')


class PasswdResetDoneView(PasswordResetDoneView):
    template_name = "authentication/password_reset_complete.html"


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "authentication/register_user.html" 
    success_url = reverse_lazy('register_me')


    def get_success_url(self):
        self.success_url = str(self.success_url + "?success")
        return super(UserCreateView, self).get_success_url()
