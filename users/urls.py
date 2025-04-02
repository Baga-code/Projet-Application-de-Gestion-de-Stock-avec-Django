from django.urls import path
from .views import inscription, connexion, deconnexion

urlpatterns = [
    path("", inscription, name="inscription"),
    path("connexion/", connexion, name="connexion"),
    path("deconnexion/", deconnexion, name="deconnexion"),
]
