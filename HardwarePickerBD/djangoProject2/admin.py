import re
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin, GroupAdmin


# Custom UserAdmin without Personal Info section
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


class MyAdminSite(AdminSite):
    site_header = _("HardwarePickerBD")
    site_title = _("Site Admin")
    index_title = _("Dashboard")

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)

        # 1. Remove "CONTENT TYPES" section
        app_list = [app for app in app_list if app['app_label'] != 'contenttypes']

        # 2. Remove Permissions from auth app
        for app in app_list:
            if app['app_label'] == 'auth':
                # Filter out Permission model
                app['models'] = [m for m in app['models'] if m['object_name'] != 'Permission']

        # 3. Clean up Guides: remove typo "Guides imagess"
        for app in app_list:
            if app['app_label'] == 'guides':
                filtered = []
                for m in app['models']:
                    if m['object_name'].lower() == 'guidesimagess':
                        continue
                    if m.get('name', '').lower() == 'guides imagess':
                        m['name'] = 'View Guides'
                    filtered.append(m)
                app['models'] = filtered

        # 4. Move CartItem, Order, OrderItem, and UserProfile
        to_move_names = {'CartItem', 'Order', 'OrderItem', 'UserProfile'}
        moved = []
        for app in app_list:
            remaining = []
            for m in app['models']:
                if m['object_name'] in to_move_names:
                    moved.append(m)
                else:
                    remaining.append(m)
            app['models'] = remaining

        # Remove any empty app sections
        app_list = [app for app in app_list if app['models']]

        # Only create "Profiles and Orders" section on main index
        if app_label is None and moved:
            app_list.append({
                'name': 'Profiles and Orders',
                'app_label': 'userprofile',
                'models': moved
            })

        return app_list


# Instantiate and configure custom admin
my_admin = MyAdminSite(name='myadmin')

# Unregister unwanted models
try:
    my_admin.unregister(ContentType)
    my_admin.unregister(Permission)  # Unregister Permission model
except Exception:
    pass

# Ensure User and Group use default admin with permissions
for model, admin_class in [(User, CustomUserAdmin), (Group, GroupAdmin)]:  # Use CustomUserAdmin
    try:
        my_admin.unregister(model)
    except admin.sites.NotRegistered:
        pass
    my_admin.register(model, admin_class)

# Register all other models
for model in apps.get_models():
    if model in (User, Group, ContentType, Permission):
        continue
    try:
        my_admin.register(model)
    except admin.sites.AlreadyRegistered:
        pass