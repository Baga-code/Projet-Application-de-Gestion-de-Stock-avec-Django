from django.urls import path
from .views import ajouter_produit, liste_produits

urlpatterns = [
    path('ajouter', ajouter_produit, name='ajouter_produit'),
    path('', liste_produits, name='liste_produits'),
]
