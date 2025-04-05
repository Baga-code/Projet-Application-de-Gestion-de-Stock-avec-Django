from django.urls import path
from .views import ajouter_produit, liste_produits, modifier_produit, supprimer_produit

urlpatterns = [
    path('', liste_produits, name='liste_produits'),
    path('ajouter', ajouter_produit, name='ajouter_produit'),
    path('modifier/<int:produit_id>/', modifier_produit, name='modifier_produit'),
    path('supprimer/<int:produit_id>/', supprimer_produit, name='supprimer_produit'),
]

