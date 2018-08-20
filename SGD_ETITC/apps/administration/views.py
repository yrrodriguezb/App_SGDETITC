from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView


class UserListView(LoginRequiredMixin, ListView):
    context_object_name = 'users'
    model = User
    paginate_by = 50
    template_name = "administration/users.html"

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        
        if query:
            qset = (
                Q(username__icontains=query) |
                Q(last_name__icontains=query)
            )
            results = User.objects.filter(qset).distinct()
        else:
            results = User.objects.all()
        return results

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['userslength'] = User.objects.count()
        context['paginate_by'] = self.get_paginate_by(None)
        context['params'] = { 
            'q' : self.request.GET.get('q', ''),
            'p' : self.request.GET.get('p', '')
        }
        return context

    def get_paginate_by(self, queryset):
        return self.request.GET.get('p', 50)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    model = User
    template_name = 'administration/edit_user.html'