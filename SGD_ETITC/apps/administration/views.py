import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView


class UserListView(LoginRequiredMixin, ListView):
    context_object_name = 'users'
    model = User
    paginate_by = 50
    template_name = "administration/users.html"

    class Meta:
        ordering = ['username', ]

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        
        if query:
            qset = (
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
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


def getUserById(request, pk):
    if request.method == 'GET' and request.is_ajax():
        try:
            user = serializers.serialize(
                "json", 
                User.objects.filter(pk=int(pk)), 
                fields=('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', )
            )

            json_data = json.loads(user)
            data = {'user': json_data[0]['fields'], 'pk': json_data[0]['pk'] }
            return JsonResponse({'ok': True, 'msg': 'Solicitud exitosa.', 'data': data })
        except:
            return JsonResponse({'ok': False, 'msg': 'Error al intentar consultar los datos.'})
    else:
        return JsonResponse({'ok': False, 'msg':'No es una solicitud válida.'})


def update_user(request, pk):
    if request.method == 'POST' and request.is_ajax():
        try:
            user = User.objects.get(pk=pk)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']

            if request.POST['is_active'] == 'false':
                user.is_active = False
            else:
                user.is_active = True

            if request.POST['is_staff'] == 'false':
                user.is_staff = False
            else:
                user.is_staff = True

            msg = 'Los datos se actualizaron correctmente. '
            email_user = User.objects.only('id').filter(email=request.POST['email']).exclude(username=user.username)

            if email_user.exists():
                msg += 'Pero el correo electronico no se actualizo, por que ya se encuentra registrado.'
            else:
                user.email = request.POST['email']

            user.save()
            return JsonResponse({'ok': True, 'msg': msg})
        except:
            return JsonResponse({'ok': False, 'msg': 'Error al intentar guardar los datos.'})
    else:
        return JsonResponse({'ok': False, 'msg':'No es una solicitud válida.'})


def delete_user(request, pk):
    if request.method == 'DELETE' and request.is_ajax():
        try:
            user = get_object_or_404(User, pk=pk)
            user.delete()
            return JsonResponse({'ok': True, 'msg': 'Los datos se eliminaron correctamente.'})
        except:
            return JsonResponse({'ok': False, 'msg': 'Error al intentar guardar los datos.'})
    else:
        return JsonResponse({'ok': False, 'msg': 'No es una solicitud válida.'})