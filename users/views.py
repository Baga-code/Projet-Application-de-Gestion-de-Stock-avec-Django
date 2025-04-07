from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Utilisateur
from .forms import *
from django.shortcuts import render
from produits.models import *
from produits.forms import *
from django.db.models import Q  
from django.core.paginator import Paginator
#from commandes.models import Commande  # Idem


User = get_user_model()

# 🔹 Vue pour l'inscription
def inscription(request):
    if request.method == "POST":
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)  # Connexion automatique après inscription
            return rediriger_utilisateur(utilisateur)  # Redirection selon le rôle
    else:
        form = FormulaireInscription()
    
    return render(request, "users/inscription.html", {"form": form}  )

# 🔹 Vue pour la connexion
def connexion(request):
    if request.method == "POST":
        form = ConnexionForm(request=request, data=request.POST)
        if form.is_valid():
            utilisateur = form.get_user()
            login(request, utilisateur)
            return rediriger_utilisateur(utilisateur)
        else:
            return render(request, "users/connexion.html", {"form": form, "erreur": "Identifiants invalides"})
    else:
        form = ConnexionForm()

    return render(request, "users/connexion.html", {"form": form})


# 🔹 Fonction de redirection selon le rôle
def rediriger_utilisateur(utilisateur):
    if utilisateur.role in [Utilisateur.ADMIN, Utilisateur.EMPLOYE]:
        return redirect("dashboard_admin")
    else:
        return redirect("dashboard_client")
# 🔹 Vue pour la déconnexion
def deconnexion(request):
    logout(request)
    return redirect("connexion")

 

def dashboard_admin(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    users = User.objects.all()
    form = ProduitForm()
    produits_alertes = Produit.objects.filter(stock__lt=5)



    # Récupération des filtres
    query = request.GET.get("q")
    categorie_id = request.GET.get("categorie")
    tri = request.GET.get("tri")
    stock = request.GET.get("stock")

    #  Recherche
    if query:
        produits = produits.filter(Q(nom__icontains=query) | Q(description__icontains=query))

    #  Filtre catégorie
    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)

    #  Filtre stock
    if stock == "rupture":
        produits = produits.filter(stock=0)
    elif stock == "faible":
        produits = produits.filter(stock__lt=5)

    #  Tri
    if tri == "nom_asc":
        produits = produits.order_by("nom")
    elif tri == "nom_desc":
        produits = produits.order_by("-nom")
    elif tri == "prix_asc":
        produits = produits.order_by("prix")
    elif tri == "prix_desc":
        produits = produits.order_by("-prix")

    #  Pagination (10 produits par page)
    paginator = Paginator(produits, 5)
    page = request.GET.get('page')
    produits_page = paginator.get_page(page)


    stats = {
        'nb_produits': produits.count(),
        'nb_commandes': 0,
        'nb_users': users.count(),
        'nb_alertes': produits_alertes.count()
    }

    context = {
        'produits': produits_page,
        'categories': categories,
        'stats': stats,
        'form': form,
        'image_form': ImageProduitForm()
    }

    return render(request, "users/dashboard_admin.html", context)



def dashboard_client(request):
    return render(request, "users/dashboard_client.html") 

