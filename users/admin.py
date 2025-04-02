from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Utilisateur

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "telephone", "date_de_naissance")
    search_fields = ("username", "email")
    list_filter = ("role",)

admin.site.register(Utilisateur, UtilisateurAdmin)
