from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

class FormulaireInscription(UserCreationForm):
    role = forms.ChoiceField(choices=Utilisateur.ROLES, label="Rôle")
    telephone = forms.CharField(max_length=15, required=False, label="Téléphone")
    adresse = forms.CharField(widget=forms.Textarea, required=False, label="Adresse")
    date_de_naissance = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Date de naissance")
    photo_profil = forms.ImageField(required=False, label="Photo de profil")

    class Meta:
        model = Utilisateur
        fields = ["username", "email", "role", "telephone", "adresse", "date_de_naissance", "photo_profil", "password1", "password2"]
