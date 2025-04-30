from django.contrib import admin
# from django.contrib import admin
# from django.contrib import admin
# Register your models here.
from .models import Procurement,Sale,CreditSale,CreditList,FAQ,Produce,Supplier,Branch
admin.site.register(Procurement)
admin.site.register(Sale)
admin.site.register(CreditSale)
admin.site.register(CreditList)
admin.site.register(FAQ)
admin.site.register(Produce)
admin.site.register(Supplier)
admin.site.register(Branch)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active', 'get_roles']
    list_filter = ['is_staff', 'is_active', 'groups']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone_number', 'is_staff', 'is_active', 'groups'),
        }),
    )
    search_fields = ['username', 'email']
    ordering = ['username']

    def get_roles(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_roles.short_description = _('Roles')
