from django.urls import path
from .views import *

urlpatterns = [
    path("", inscription, name="inscription"),
    path("connexion/", connexion, name="connexion"),
    path("deconnexion/", deconnexion, name="deconnexion"),
    path("dashboard_admin/", dashboard_admin, name="dashboard_admin"),
    path("dashboard_client/", dashboard_client, name="dashboard_client"),
    path("utilisateurs/", liste_utilisateurs, name="liste_utilisateurs"),
    path("utilisateurs/<int:utilisateur_id>/changer-role/", changer_role_utilisateur, name="changer_role_utilisateur"),
    path("utilisateurs/<int:utilisateur_id>/supprimer/", supprimer_utilisateur, name="supprimer_utilisateur"),
    path("historique/", historique_actions, name="historique_actions"),

]
