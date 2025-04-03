from django.db import models

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
