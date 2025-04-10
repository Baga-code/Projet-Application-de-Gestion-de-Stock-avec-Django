from django import forms
from .models import Produit, ImageProduit, Commande

# Formulaire pour la création/modification des produits
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'stock', 'categorie']  # Correction du champ 'quantite' -> 'stock'

# Formulaire pour l'ajout d'images associées à un produit
class ImageProduitForm(forms.ModelForm):
    class Meta:
        model = ImageProduit
        fields = ['image']

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['produit', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'quantite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
