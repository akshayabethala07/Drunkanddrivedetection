# users/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import ClientRegister_Model


class CustomUserAdmin(UserAdmin):
    model = ClientRegister_Model
    list_display = ['username', 'email', 'phoneno', 'country', 'state', 'city', 'address', 'gender', 'is_staff',
                    'is_active']
    fieldsets = (
        (None,
         {'fields': ('username', 'email', 'password', 'phoneno', 'country', 'state', 'city', 'address', 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups')}),  # Include groups field here
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'email', 'password1', 'password2', 'phoneno', 'country', 'state', 'city', 'address', 'gender',
            'is_staff', 'is_active', 'groups')}
         ),
    )
    search_fields = ('username', 'email', 'phoneno')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new user
            obj.set_password(form.cleaned_data['password1'])  # Set password
        super().save_model(request, obj, form, change)


# Customize the Group admin to allow selection of users
class GroupAdmin(admin.ModelAdmin):
    model = Group
    filter_horizontal = ('permissions',)  # This adds a multi-select for permissions
    list_display = ['name']  # Add other fields if necessary


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

admin.site.register(ClientRegister_Model, CustomUserAdmin)
