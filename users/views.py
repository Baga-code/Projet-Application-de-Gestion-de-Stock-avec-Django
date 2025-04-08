from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Utilisateur
from .forms import *
from django.shortcuts import render
from produits.models import *
from produits.forms import *
from django.db.models import Q  
from django.core.paginator import Paginator
from django.contrib import messages
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


#  Fonction de redirection selon le rôle
def rediriger_utilisateur(utilisateur):
    if utilisateur.role in [Utilisateur.ADMIN, Utilisateur.EMPLOYE]:
        return redirect("dashboard_admin")
    else:
        return redirect("dashboard_client")
#  Vue pour la déconnexion
def deconnexion(request):
    logout(request)
    return redirect("connexion")

 

def dashboard_admin(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    users = User.objects.all()
    form = ProduitForm()

    # Vérifie si on veut filtrer les produits à stock faible
    stock = request.GET.get("stock")
    if stock == "faible":
        produits = produits.filter(stock__lte=5)

    # Autres filtres
    query = request.GET.get("q")
    categorie_id = request.GET.get("categorie")
    tri = request.GET.get("tri")

    if query:
        produits = produits.filter(Q(nom__icontains=query) | Q(description__icontains=query))

    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)

    if tri == "nom_asc":
        produits = produits.order_by("nom")
    elif tri == "nom_desc":
        produits = produits.order_by("-nom")
    elif tri == "prix_asc":
        produits = produits.order_by("prix")
    elif tri == "prix_desc":
        produits = produits.order_by("-prix")

    # Pagination
    paginator = Paginator(produits, 5)
    page = request.GET.get('page')
    produits_page = paginator.get_page(page)

    # Alerte stock
    alerte_popup = AlerteStock.objects.count() > 0 and stock != "faible"

    # Statistiques
    stats = {
        'nb_produits': produits.count(),
        'nb_commandes': 0,
        'nb_users': users.count(),
        'nb_alertes': AlerteStock.objects.count()
    }

    # Graphique stock par produit (non paginé, sans filtre)
    tous_les_produits = Produit.objects.all()
    labels = [p.nom for p in tous_les_produits]
    stocks = [p.quantite_stock for p in tous_les_produits]
    colors = [
        'rgba(255, 99, 132, 0.7)' if p.quantite_stock <= 5 else 'rgba(54, 162, 235, 0.7)'
        for p in tous_les_produits
    ]

    context = {
        'produits': produits_page,
        'categories': categories,
        'stats': stats,
        'form': form,
        'image_form': ImageProduitForm(),
        'alerte_popup': alerte_popup,
        'labels': labels,
        'stocks': stocks,
        'colors': colors,
    }

    return render(request, "users/dashboard_admin.html", context)




def dashboard_client(request):
    return render(request, "users/dashboard_client.html") 

