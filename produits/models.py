from django.db import models
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Modèle représentant une catégorie de produits
class Categorie(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

# Modèle représentant un produit
class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()  # Correction: "quantite" remplacé par "stock"
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='produits')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

# Modèle représentant les images d'un produit
class ImageProduit(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='produits/')
    date_ajout = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Image de {self.produit.nom}"
    

# Historique des actions sur un produit
class HistoriqueProduit(models.Model):
    ACTIONS = (
        ('ajout', 'Ajout'),
        ('modification', 'Modification'),
        ('suppression', 'Suppression'),
    )

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTIONS)
    date_action = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.action} - {self.produit.nom}"

# Alerte automatique si stock bas
class AlerteStock(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    stock_actuel = models.PositiveIntegerField()
    date_alerte = models.DateTimeField(auto_now_add=True)
    seuil = models.PositiveIntegerField(default=5)  # Personnalisable si besoin

    def __str__(self):
        return f"Alerte: {self.produit.nom} stock bas ({self.stock_actuel})"


# Historique automatique à la sauvegarde
@receiver(post_save, sender=Produit)
def enregistrer_modification_produit(sender, instance, created, **kwargs):
    from users.models import get_current_user  # à créer via middleware si tu veux
    user = get_current_user()
    if user:
        action = 'ajout' if created else 'modification'
        HistoriqueProduit.objects.create(utilisateur=user, produit=instance, action=action)

    # Vérifier le stock et générer une alerte si nécessaire
    if instance.stock <= 5:
        AlerteStock.objects.create(produit=instance, stock_actuel=instance.stock)

@receiver(post_delete, sender=Produit)
def enregistrer_suppression_produit(sender, instance, **kwargs):
    from users.models import get_current_user  # à créer via middleware si tu veux
    user = get_current_user()
    if user:
        HistoriqueProduit.objects.create(utilisateur=user, produit=instance, action='suppression')