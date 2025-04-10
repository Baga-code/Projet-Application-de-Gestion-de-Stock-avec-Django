from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ADMIN = "admin"
    EMPLOYE = "employe"
    CLIENT = "client"

    ROLES = [
        (ADMIN, "Administrateur"),
        (EMPLOYE, "Employé"),
        (CLIENT, "Client"),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default=CLIENT)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    date_de_naissance = models.DateField(blank=True, null=True)
    photo_profil = models.ImageField(upload_to="photos_profils/", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Synchronisation role-admin ↔ superuser
        if self.role == self.ADMIN:
            self.is_superuser = True
            self.is_staff = True
        else:
            self.is_superuser = False  
            self.is_staff = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
