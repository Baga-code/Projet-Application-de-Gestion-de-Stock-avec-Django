from django.urls import path
from .views import *

urlpatterns = [
    path("", inscription, name="inscription"),
    path("connexion/", connexion, name="connexion"),
    path("deconnexion/", deconnexion, name="deconnexion"),
    path("dashboard_admin/", dashboard_admin, name="dashboard_admin"),
    path("dashboard_client/", dashboard_client, name="dashboard_client"),
]
