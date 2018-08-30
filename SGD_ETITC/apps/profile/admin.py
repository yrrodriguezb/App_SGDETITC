from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
  fields = ['user', 'avatar', 'birthdate', 'phone', 'cellphone', 'created', 'updated', ]
  list_display = ('user', 'birthdate', 'phone', 'avatar',)
  ordering = ['user', ]
  search_fields = ['user__username', ]
  readonly_fields = ['created', 'updated', 'user',]

  def get_actions(self, request):
      actions = super(ProfileAdmin, self).get_actions(request) # Obtenemos todas las acciones de este modelo
      del actions['delete_selected'] # Deshabilitamos la opción de borrar
      return actions
      
  def has_delete_permission(self, request, obj=None):
      return False


admin.site.register(Profile, ProfileAdmin)
