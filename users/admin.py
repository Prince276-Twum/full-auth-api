from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


@admin.register(models.UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name"]
