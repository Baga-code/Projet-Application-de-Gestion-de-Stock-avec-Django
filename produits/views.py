from django.shortcuts import render, redirect , get_object_or_404
from .forms import ProduitForm, ImageProduitForm
from .models import Produit , Categorie
from django.core.paginator import Paginator
from django.contrib import messages
 
def ajouter_produit(request):
    if request.method == "POST" and request.user.is_superuser:
        form = ProduitForm(request.POST)
        image_form = ImageProduitForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            produit = form.save(commit=False)
            produit.save()

            image = image_form.save(commit=False)
            image.produit = produit
            image.save()

            messages.success(request, "✅ Produit ajouté avec succès.")
            return redirect("dashboard_admin")   
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs du formulaire.")
    
    return redirect("dashboard_admin")

def liste_produits(request):
    produits_list = Produit.objects.all().order_by('-date_ajout')
    paginator = Paginator(produits_list, 10)
    page = request.GET.get('page')
    produits = paginator.get_page(page)

    # Formulaire d'ajout (statique)
    form_produit = ProduitForm()
    form_image = ImageProduitForm()

    # Liste des catégories pour le modal d'édition
    categories = Categorie.objects.all()

    return render(request, 'users/dashbord_admin.html', {
        'produits': produits,
        'form_produit': form_produit,
        'form_image': form_image,
        'categories': categories,
    })

def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produits/modifier.html', {'form': form, 'produit': produit})

def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == "POST":
        produit.delete()
        return redirect('liste_produits')
    return render(request, 'produits/supprimer.html', {'produit': produit})




