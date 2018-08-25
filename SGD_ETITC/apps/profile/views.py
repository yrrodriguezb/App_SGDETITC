from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from .forms import ProfileForm
from .models import Profile


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'profile/profile_detail.html'
    

    def get_object(self):
        profile = get_object_or_404(Profile, user__username=self.request.user.username)
        return profile


@login_required
def update_profile(request, pk):
    alert_data = { 'icon': 'warning', 'color': 'error' }
    json_response = { 'ok': False, 'msg': 'El metodo de petición es incorrecto.', 'alert': alert_data }

    try:
        if request.method == 'POST':
            profile = get_object_or_404(Profile, pk=pk)
            user_by_email = User.objects.only('id').filter(email=request.POST.get('email', None)).exclude(username=request.user)
           
            if profile.user != request.user:
                json_response = { 'ok': False, 'msg': 'No puede modificar el perfil de usuario.', 'alert': alert_data }
            elif request.POST.get('email', '') is not '' and user_by_email.exists():
                json_response = { 'ok': False, 'msg': 'El email no se encuentra disponible.', 'alert': alert_data }
            else:
                form = ProfileForm(request.POST, files=request.FILES, instance=profile)

                if form.is_valid():
                    form.save()

                    alert_data = { 'icon': 'check_circle', 'color': 'success' }
                    json_response = { 'ok': True, 'msg': 'Los datos se guardaron correctamente.', 'data': form.data, 'alert': alert_data }

                    if request.FILES:
                        profile.avatar = request.FILES['file']
                        profile.save()
                        json_response.update({ 'file': request.FILES['file'].name })
                else:
                    json_response = { 'ok': False, 'msg': 'Los datos del formulario no son validos.', 'alert': alert_data }
                    json_response.update({'errors': form.errors})
    except:
        alert_data = { 'icon': 'warning', 'color': 'error' }
        json_response = { 'ok': False, 'msg': 'Ocurrio un error al intentar guardar los cambios.' , 'alert': alert_data  }


    return JsonResponse(json_response)

        

