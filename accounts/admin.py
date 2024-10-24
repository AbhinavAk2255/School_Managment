from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.


admin.site.register(FeesHistory)
admin.site.register(LibraryHistory)
admin.site.register(Library)

# Ensure admin can create and manage staff and librarian accounts
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'role', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'confirm_password', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'current_class', 'admission_number')