from django.shortcuts import render, redirect , get_object_or_404, HttpResponse
from .forms import ProduitForm, ImageProduitForm, CommandeForm
from .models import *
from django.core.paginator import Paginator
from django.contrib import messages
import csv
import json
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

 
def ajouter_produit(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès non autorisé.")
        return redirect("")

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
            return redirect("dashboard_admin")

        messages.error(request, "Erreur dans le formulaire.")

    else:
        form = ProduitForm()
        image_form = ImageProduitForm()

    return render(request, "produits/ajout.html", {
        "form": form,
        "image_form": image_form
    })


def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == "POST":
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()

            if produit.stock <= 5:
                AlerteStock.objects.update_or_create(
                    produit=produit,
                    defaults={"stock_actuel": produit.stock}
                )
            else:
                AlerteStock.objects.filter(produit=produit).delete()

            # Ajout à l’historique
            HistoriqueProduit.objects.create(
                utilisateur=request.user,
                produit=produit,
                action="modification"
            )

            messages.success(request, "Produit modifié avec succès ✅.")
            return redirect('dashboard_admin')  
    else:
        form = ProduitForm(instance=produit)

    return render(request, 'produits/modifier.html', {'form': form, 'produit': produit})

def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    if request.method == "POST":
        nom_produit = produit.nom 
        
        
        # Ajout à l’historique
        HistoriqueProduit.objects.create(
            utilisateur=request.user,
            produit=produit,
            action="suppression"
        )
#Apres la sauvegarde de l'historique, on supprime le produit
        produit.delete()
        
        messages.success(request, f"Le produit '{nom_produit}' a été supprimé avec succès ✅.")
        return redirect('dashboard_admin')
    return render(request, 'produits/supprimer.html', {'produit': produit})

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="produits.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nom', 'Prix', 'Stock'])  

    for produit in Produit.objects.all():
        writer.writerow([produit.nom, produit.prix, produit.stock])

    # Ajout à l’historique
    HistoriqueProduit.objects.create(
        utilisateur=request.user,
        produit=produit,
        action="exporter en CSV"
    )
    return response

def export_pdf(request):
    produits = Produit.objects.all().order_by('id') 
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

    # Gestion des erreurs
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération du PDF', status=500)
    return response



@login_required(login_url='connexion')
def passer_commande(request):
    if request.method == 'POST':
        form = CommandeForm(request.POST)
        if form.is_valid():
            produit = form.cleaned_data['produit']
            quantite = form.cleaned_data['quantite']

            if produit.stock >= quantite:
                # Mise à jour du stock
                produit.stock -= quantite
                produit.save()

                # Enregistrement de la commande
                commande = form.save(commit=False)
                commande.utilisateur = request.user
                commande.save()

                messages.success(request, f"✅ Commande de {quantite} x {produit.nom} enregistrée avec succès.")
                return redirect('dashboard_admin')
            else:
                messages.warning(request, f"❌ Stock insuffisant : il ne reste que {produit.stock} unités de {produit.nom}.")
    else:
        form = CommandeForm()

    return render(request, 'commandes/passer_commande.html', {'form': form})


@login_required(login_url='connexion') 
def liste_commandes(request):
    commandes = Commande.objects.filter(utilisateur=request.user).order_by('-date_commande')
    return render(request, 'commandes/liste_commande.html', {'commandes': commandes})
