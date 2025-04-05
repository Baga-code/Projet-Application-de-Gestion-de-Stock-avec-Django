from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Utilisateur
from .forms import FormulaireInscription , ConnexionForm
from django.shortcuts import render
from produits.models import Produit, Categorie   
from produits.forms import ProduitForm  , ImageProduitForm
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
    form = ProduitForm()  # ✅ formulaire vierge pour la modale

    stats = {
        'nb_produits': produits.count(),
        'nb_commandes': 0,
        'nb_users': users.count(),
        'nb_alertes': produits.filter(stock__lt=5).count()
    }

    context = {
    'produits': produits,
    'categories': categories,
    'stats': stats,
    'form': ProduitForm(),
    'image_form': ImageProduitForm()
}
    

    return render(request, "users/dashboard_admin.html", context)


def dashboard_client(request):
    return render(request, "users/dashboard_client.html")
