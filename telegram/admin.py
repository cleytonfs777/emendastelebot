from django.contrib import admin

from .models import Registrador


@admin.register(Registrador)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('user_ident', 'nomeuser', 'data', 'tipo')