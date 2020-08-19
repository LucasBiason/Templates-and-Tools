from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from users import models

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display =  ['username', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields':('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'), 
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
    )

admin.site.register(models.User, UserAdmin)
