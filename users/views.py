from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Utilisateur
from .forms import FormulaireInscription

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
        username = request.POST["username"]
        password = request.POST["password"]
        utilisateur = authenticate(request, username=username, password=password)

        if utilisateur is not None:
            login(request, utilisateur)
            return rediriger_utilisateur(utilisateur)  # Redirection selon le rôle
        else:
            return render(request, "users/connexion.html", {"erreur": "Identifiants invalides"})

    return render(request, "users/connexion.html")

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
