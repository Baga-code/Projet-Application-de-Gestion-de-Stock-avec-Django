from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm

# Formulaire d'inscription
class FormulaireInscription(UserCreationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom d’utilisateur'
        })
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre adresse email'
        })
    )

    role = forms.ChoiceField(
        choices=Utilisateur.ROLES, 
        label="Rôle")
    
    telephone = forms.CharField(
        max_length=15, required=False, 
        label="Téléphone",  widget=forms.TextInput(attrs={
            'placeholder': 'Entrez votre Numéro de Téléphone',
            'class': 'form-control'
        }))
    adresse = forms.CharField(max_length=255, required=False, label="Adresse",widget=forms.TextInput(attrs={
            'placeholder': 'Entrez votre Adresse',
            'class': 'form-control'
        }))
    date_de_naissance = forms.DateField(
        required=False,
          widget=forms.DateInput(attrs={'type': 'date'}), label="Date de naissance")
    
    photo_profil = forms.ImageField(required=False, label="Photo de profil")
    
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Créez un mot de passe sécurisé'
        })
    )

    password2 = forms.CharField(
        label="Confirmation mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmez votre mot de passe'
        })
    )


    class Meta:
        model = Utilisateur
        fields = ["username", "email", "role", "telephone", "adresse", "date_de_naissance", "photo_profil", "password1", "password2"]

# Formulaire de connexion
class ConnexionForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre nom d’utilisateur'
        })
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre mot de passe'
        })
    )