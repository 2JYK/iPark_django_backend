from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User as UserModel


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'fullname', 'email')
    list_display_links = ('username',)
    list_filter = ('username',)
    search_fields = ('username', 'email', )
    
    fieldsets = (
        ("info", {"fields": ("username", "fullname", "password", "email", "phone", "region", "join_date", )}),
        ("Permissions", {"fields": ("is_admin", "is_active", )}),)
    
    filter_horizontal = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date',)
        else:
            return ('join_date', )


admin.site.register(UserModel, UserAdmin)