from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def custom_upload_to(instance, filename):
    old_instance = Profile.objects.get(pk=instance.pk)
    old_instance.avatar.delete()
    return 'profiles/' + filename


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    avatar = models.ImageField(upload_to=custom_upload_to, null=True, blank=True, verbose_name='Imagen')
    birthdate = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name='Fecha de Nacimiento')
    cellphone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Celular")
    created = models.DateTimeField(auto_now=True, verbose_name="Fecha de creación")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Teléfono")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de Edición")

    class Meta:
        ordering = ['user__username',]
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"

    def __str__(self):
        return self.user.username


""" Señal que se encarga de crearun perfil cuando se cree un usuario """
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    # Valida que tenga el atributo created para indicar que se ha crado por primera vez.
    # Sino existe devolvemos false cpor defecto
    if kwargs.get('created', False):
        Profile.objects.get_or_create(user=instance)
        #print('Se acaba de crear un usuario con su perfil enlazado')



