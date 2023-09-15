from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in models.CustomUser._meta.fields]
    #list_display_links = ['password']
    #exclude = ["password"]

    list_display = ["id", "username", "birthdate"]