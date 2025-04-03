from django.shortcuts import render, redirect
from .forms import ProduitForm, ImageProduitForm
from .models import Produit

def ajouter_produit(request):
    if request.method == "POST":
        form_produit = ProduitForm(request.POST)
        form_image = ImageProduitForm(request.POST, request.FILES)

        if form_produit.is_valid() and form_image.is_valid():
            produit = form_produit.save()  # Sauvegarde du produit
            image = form_image.save(commit=False)
            image.produit = produit  # Associer l'image au produit créé
            image.save()
            return redirect('liste_produits')  # Redirection après succès

    else:
        form_produit = ProduitForm()
        form_image = ImageProduitForm()

    return render(request, 'produits/ajout.html', {'form_produit': form_produit, 'form_image': form_image})

def liste_produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits/liste.html', {'produits': produits})
