from django.contrib import admin
from .models import *

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


@admin.register(HistoriqueProduit)
class HistoriqueProduitAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'produit', 'action', 'date_action')
    list_filter = ('action', 'date_action')
    search_fields = ('utilisateur__username', 'produit__nom', 'action')
    readonly_fields = ('utilisateur', 'produit', 'action', 'date_action')  # Rendre ces champs en lecture seule

@admin.register(AlerteStock)
class AlerteStockAdmin(admin.ModelAdmin):
    list_display = ('produit', 'stock_actuel', 'seuil', 'date_alerte')
    list_filter = ('date_alerte',)
    search_fields = ('produit__nom',)
    readonly_fields = ('produit', 'stock_actuel', 'date_alerte')  # Rendre ces champs en lecture seule


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'produit', 'quantite', 'date_commande')
    list_filter = ('date_commande',)
 