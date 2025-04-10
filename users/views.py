from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Utilisateur
from .forms import *
from produits.models import *
from produits.forms import *
from django.db.models import Q  
from django.core.paginator import Paginator
from django.contrib import messages
import json
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


User = get_user_model()

#  Vue pour l'inscription
def inscription(request):
    if request.user.is_authenticated:
        return rediriger_utilisateur(request.user)  # redirige vers dashboard si l'utilisateur est connecté
    
    if request.method == "POST":
        form = FormulaireInscription(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            login(request, utilisateur)  # Connexion automatique après inscription
            return rediriger_utilisateur(utilisateur)  # Redirection selon le rôle
    else:
        form = FormulaireInscription()
    
    return render(request, "users/inscription.html", {"form": form}  )

#  Vue pour la connexion
def connexion(request):
    if request.user.is_authenticated:
        return rediriger_utilisateur(request.user)  # redirige vers dashboard si l'utilisateur est connecté
    
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
    
@login_required(login_url='connexion')
def liste_utilisateurs(request):
    utilisateurs = Utilisateur.objects.all()

    # Vérifie si l'utilisateur connecté peut modifier
    peut_modifier = request.user.is_superuser

    return render(request, "users/liste_user.html", {
        "utilisateurs": utilisateurs,
        "peut_modifier": peut_modifier,
    })

@login_required
def changer_role_utilisateur(request, utilisateur_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas la permission.")

    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)
    nouveau_role = request.POST.get("role")

    if nouveau_role in dict(Utilisateur.ROLES):
        utilisateur.role = nouveau_role
        utilisateur.save()

    return redirect("liste_utilisateurs")


@login_required
def supprimer_utilisateur(request, utilisateur_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Vous n'avez pas la permission.")

    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)
    if utilisateur != request.user:  # sécurité pour ne pas se supprimer soi-même
        utilisateur.delete()

    return redirect("liste_utilisateurs")


#  Vue pour la déconnexion
def deconnexion(request):
    logout(request)
    return redirect("connexion")

 
@login_required(login_url='connexion')
def dashboard_admin(request):
    produits = Produit.objects.all()
    categories = Categorie.objects.all()
    users = get_user_model().objects.all()
    form = ProduitForm()

    # Filtre stock faible
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
        'nb_commandes': Commande.objects.count(),
        'nb_users': users.count(),
        'nb_alertes': AlerteStock.objects.count()
    }

    # === GRAPH PRODUITS ===
    tous_les_produits = Produit.objects.all()
    labels = [p.nom for p in tous_les_produits]
    stocks = [p.stock for p in tous_les_produits]
    colors = [
        'rgba(255, 99, 132, 0.7)' if p.stock <= 5 else 'rgba(54, 162, 235, 0.7)'
        for p in tous_les_produits
    ]

    context = {
        'produits': produits_page,
        'categories': categories,
        'stats': stats,
        'form': form,
        'image_form': ImageProduitForm(),
        'alerte_popup': alerte_popup,
        'labels': json.dumps(labels),
        'stocks': json.dumps(stocks),
        'colors': json.dumps(colors),
    }

    return render(request, "users/dashboard_admin.html", context)


@login_required(login_url='connexion')
def dashboard_client(request):
    return render(request, "users/dashboard_client.html") 


@login_required(login_url='connexion')
def historique_actions(request):
    historique = HistoriqueProduit.objects.select_related('utilisateur', 'produit').order_by('-date_action')
    return render(request, "admin/historique_actions.html", {
        "historique": historique
    })

