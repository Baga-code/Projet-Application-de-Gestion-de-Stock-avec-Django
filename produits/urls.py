from django.urls import path
from .views import  *
urlpatterns = [
    path('ajouter', ajouter_produit, name='ajouter_produit'),
    path('modifier/<int:produit_id>/', modifier_produit, name='modifier_produit'),
    path('supprimer/<int:produit_id>/', supprimer_produit, name='supprimer_produit'),
    path('export/csv/', export_csv, name='export_csv'),
    path('export/pdf/', export_pdf, name='export_pdf'),
    path('commande/', passer_commande, name='passer_commande'),
    path('commandes/', liste_commandes, name='liste_commandes'),
]

