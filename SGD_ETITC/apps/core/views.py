from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'title': 'App SGD - ETITC'})

@login_required
def send_email(request):
    if request.is_ajax():
        subject = request.GET.get('subject')
        message = request.GET.get('message')
        from_email = request.GET.get('from_email')
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, ['django.yrrodriguezb@gmail.com'])
            except BadHeaderError:
                return JsonResponsen({'ok': False, 'type': 'error', 'msg': 'Ocurrio un error al enviar el mensaje.'})
            return JsonResponse({'ok': True, 'type': 'success', 'msg': 'El mensaje de ha enviado correctamente a ' + str(from_email) } )
        else:
            return JsonResponse({'ok': False, 'type': 'error', 'msg': 'Datos incompletos, por favor diligenciar todos los campos.'})

    return HttpResponseBadRequest()