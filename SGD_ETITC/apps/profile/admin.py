from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
  ordering = ['created', ]
  search_fields = ['user__username', ]
  readonly_fields = ['created', 'updated', ]


admin.site.register(Profile, ProfileAdmin)
