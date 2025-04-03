from django.contrib import admin
from .models import Produit, Categorie, ImageProduit

# Enregistrement des modèles dans l'interface admin
@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'stock', 'categorie', 'date_ajout')
    list_filter = ('categorie', 'date_ajout')
    search_fields = ('nom', 'description')

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom',)

@admin.register(ImageProduit)
class ImageProduitAdmin(admin.ModelAdmin):
    list_display = ('produit', 'image', 'date_ajout')
