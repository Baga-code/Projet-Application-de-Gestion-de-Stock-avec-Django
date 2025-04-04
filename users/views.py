from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Utilisateur
from .forms import FormulaireInscription , ConnexionForm

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
from django.shortcuts import render

def dashboard_admin(request):
    return render(request, "users/dashboard_admin.html")

def dashboard_client(request):
    return render(request, "users/dashboard_client.html")
