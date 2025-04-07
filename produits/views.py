from django.shortcuts import render, redirect , get_object_or_404, HttpResponse
from .forms import ProduitForm, ImageProduitForm
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
import csv
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib.auth import get_user_model

 
def ajouter_produit(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès non autorisé.")
        return redirect("liste_produits")

    if request.method == "POST":
        form = ProduitForm(request.POST)
        image_form = ImageProduitForm(request.POST, request.FILES)

        if form.is_valid() and image_form.is_valid():
            produit = form.save()

            # Sauvegarde image
            image = image_form.save(commit=False)
            image.produit = produit
            image.save()

            # Ajout à l’historique
            HistoriqueProduit.objects.create(
                utilisateur=request.user,
                produit=produit,
                action="ajout"
            )

            # Vérifie le stock
            if produit.stock <= 5:
                AlerteStock.objects.create(
                    produit=produit,
                    stock_actuel=produit.stock
                )

            messages.success(request, "Produit ajouté avec succès ✅ .")
            return redirect("liste_produits")

        messages.error(request, "Erreur dans le formulaire.")

    else:
        form = ProduitForm()
        image_form = ImageProduitForm()

    return render(request, "produits/ajout.html", {
        "form": form,
        "image_form": image_form
    })

def liste_produits(request):
    produits_list = Produit.objects.all().order_by('id')
    paginator = Paginator(produits_list, 5)
    page = request.GET.get('page')
    produits = paginator.get_page(page)

    form_produit = ProduitForm()
    form_image = ImageProduitForm()
    categories = Categorie.objects.all()

    # Construction des statistiques
    User = get_user_model()
    stats = {
        'nb_produits': Produit.objects.count(),
        'nb_commandes': 0,  # si tu as un modèle Commande, remplace 0 par Commande.objects.count()
        'nb_users': User.objects.count(),
        'nb_alertes': AlerteStock.objects.count(),
    }

    return render(request, 'users/dashboard_admin.html', {
        'produits': produits,
        'form_produit': form_produit,
        'form_image': form_image,
        'categories': categories,
        'stats': stats,
    })

def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, "Produit modifié avec succès ✅.")
            return redirect('liste_produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produits/modifier.html', {'form': form, 'produit': produit})

def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == "POST":
        nom_produit = produit.nom  # On garde le nom pour le message après suppression
        produit.delete()
        messages.success(request, f"Le produit '{nom_produit}' a été supprimé avec succès ✅.")
        return redirect('liste_produits')
    return render(request, 'produits/supprimer.html', {'produit': produit})

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produits.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prix', 'Stock'])  # Ajouter les champs souhaités

    for produit in Produit.objects.all():
        writer.writerow([produit.nom, produit.prix, produit.stock])

    return response

def export_pdf(request):
    produits = Produit.objects.all().order_by('id')  # Trier par ID croissant
    template_path = 'produits/pdf_template.html'
    context = {'produits': produits}

    # Préparation de la réponse HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="produits.pdf"'

    # Chargement du template Django
    template = get_template(template_path)
    html = template.render(context)

    # Génération du PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    

    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response