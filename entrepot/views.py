from math import sumprod
from pyexpat.errors import messages
from time import timezone
from urllib import response
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from .models import Absence, Avance, Produit, Client, Fournisseur, Centre, Employe, Achat, Reglement, ReglementClient, Transfert, Vente
from .forms import  AbsenceForm, AvanceForm, FilterForm, PaiementCreditForm, ProduitForm, ClientForm, FournisseurForm, CentreForm, EmployeForm, AchatForm, ReglementForm, ReglementVenteForm, TransfertFilterForm, TransfertForm, VenteForm
from django.db.models import Sum

def base_view(request):
    return render(request, 'base.html')


def list_produits(request):
    produits = Produit.objects.all()
    # Par défaut, affichez tous les clients (supprimés et non supprimés)
    show_deleted = request.GET.get('show_deleted', False)

    if not show_deleted:
        # Si vous ne souhaitez pas afficher les clients supprimés, filtrez-les
        produits = produits.filter(isDeleted = False)

    return render(request, 'produits/ProdList.html', {'produits': produits, 'show_deleted': show_deleted})


def create_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ProdList")
    else:
        form = ProduitForm()
    return render(request, 'produits/ProdCreate.html', {'form': form})

def update_produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            return redirect("ProdList")
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'produits/ProdEdit.html', {'form': form})

def delete_produit(request,produit_id):
    produit=Produit.objects.get(id=produit_id)
    if request.method == 'POST':
        
        #produit.delete()
        produit.isDeleted = True
        produit.save()
        return redirect('ProdList')
    else:
        return render(request, 'produits/ProdDelete.html', {'produit': produit})



from django.shortcuts import render, get_object_or_404
from .models import Employe
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from .models import Employe
from django.utils import timezone

def list_employes(request):
    show_deleted = request.GET.get('show_deleted', False)
    employes = Employe.objects.all()
      
    employes_with_salaire = []  # Liste pour stocker les informations de chaque employé avec le salaire mensuel
    if not show_deleted:

        employes = employes.filter(isDeleted=False)
    
    
    for employe in employes:

        nombre_absence = employe.nombreAbscence if employe.nombreAbscence is not None else 0

        avance_demandee = Avance.objects.filter(employe=employe).aggregate(Sum('montant'))['montant__sum'] or 0
        employe.salaire_jour -= avance_demandee
        salaire_mois = employe.salaire_jour * (29 - nombre_absence) + (employe.salaire_jour - avance_demandee)
                                                                       
        employes_with_salaire.append({'employe': employe, 'salaire_mois': salaire_mois})

    print(f"List: {employes_with_salaire}")
    print(f"nb: {nombre_absence}")
    return render(request, 'employes/EmpList.html', {'employes':   employes_with_salaire, 'show_deleted': show_deleted})

def create_employe(request):
    if request.method == 'POST':
        form = EmployeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("EmpList")
    else:
        form = EmployeForm()
    return render(request, 'employes/EmpCreate.html', {'form': form})

def update_employe(request, employe_id):
    employe = Employe.objects.get(id=employe_id)
    if request.method == 'POST':
        form = EmployeForm(request.POST, instance=employe)
        if form.is_valid():
            form.save()
            return redirect("EmpList")
    else:
        form = EmployeForm(instance=employe)
    return render(request, 'employes/EmpEdit.html', {'form': form})

def delete_employe(request,employe_id):
    employe=Employe.objects.get(id=employe_id)
    if request.method == 'POST':
        
        #employe.delete()
        employe.isDeleted = True
        employe.save()
        return redirect('EmpList')
    else:
        return render(request, 'employes/EmpDelete.html', {'employe': employe})



def list_clients(request):
    # Récupérez tous les clients (y compris ceux supprimés)
    clients = Client.objects.all()

    # Par défaut, affichez tous les clients (supprimés et non supprimés)
    show_deleted = request.GET.get('show_deleted', False)

    if not show_deleted:
        # Si vous ne souhaitez pas afficher les clients supprimés, filtrez-les
        clients = clients.filter(isDeleted = False)

    return render(request, 'clients/ClientList.html', {'clients': clients, 'show_deleted': show_deleted})

def create_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("ClientList")
    else:
        form = ClientForm()
    return render(request, 'clients/ClientCreate.html', {'form': form})

def update_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("ClientList")
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/ClientEdit.html', {'form': form})

def delete_client(request, client_id):
    client=Client.objects.get(id=client_id)
    if request.method == 'POST':
        
        #client.delete()
        client.isDeleted = True
        client.save()
        return redirect('ClientList')
    else:
        
        return render(request, 'clients/ClientDelete.html', {'client': client})



def list_centres(request):
    centres = Centre.objects.all()
    # Par défaut, affichez tous les clients (supprimés et non supprimés)
    show_deleted = request.GET.get('show_deleted', False)

    if not show_deleted:
        # Si vous ne souhaitez pas afficher les clients supprimés, filtrez-les
        centres = centres.filter(isDeleted = False)

    return render(request, 'centres/CentreList.html', {'centres': centres})

def create_centre(request):
    if request.method == 'POST':
        form = CentreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("CentreList")
    else:
        form = CentreForm()
    return render(request, 'centres/CentreCreate.html', {'form': form})

def update_centre(request, centre_id):
    centre = Centre.objects.get(id=centre_id)
    if request.method == 'POST':
        form = CentreForm(request.POST, instance=centre)
        if form.is_valid():
            form.save()
            return redirect("CentreList")
    else:
        form = CentreForm(instance=centre)
    return render(request, 'centres/CentreEdit.html', {'form': form})

def delete_centre(request,centre_id):
    centre=Centre.objects.get(id=centre_id)
    if request.method == 'POST':
        
        #centre.delete()
        centre.isDeleted = True
        centre.save()
        return redirect('CentreList')
    else:
        return render(request, 'centres/CentreDelete.html', {'centre': centre})

def list_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'fournisseurs/FourList.html', {'fournisseurs': fournisseurs})

def create_fournisseur(request):
    if request.method == 'POST':
        form = FournisseurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("FourList")
    else:
        form = FournisseurForm()
    return render(request, 'fournisseurs/FourCreate.html', {'form': form})

def update_fournisseur(request, fournisseur_id):
    fournisseur = Fournisseur.objects.get(id=fournisseur_id)
    if request.method == 'POST':
        form = FournisseurForm(request.POST, instance=fournisseur)
        if form.is_valid():
            form.save()
            return redirect("FourList")
    else:
        form = FournisseurForm(instance=fournisseur)
    return render(request, 'fournisseurs/FourEdit.html', {'form': form})

def delete_fournisseur(request,fournisseur_id):
    fournisseur=Fournisseur.objects.get(id=fournisseur_id)
    if request.method == 'POST':
        
        fournisseur.delete()
        return redirect('FourList')
    else:
        return render(request, 'fournisseurs/FourDelete.html', {'fournisseur': fournisseur})

def acheter_matiere(request):
    if request.method == 'POST':
        achat_form = AchatForm(request.POST)
        if achat_form.is_valid():
            achat = achat_form.save(commit=False)
            
            # Calculer le montant total en fonction de la quantité et du prix unitaire
            achat.montant_total_ht = achat.quantite * achat.prix_unitaire_ht
            achat.save()

            # Mise à jour du solde fournisseur
            fournisseur = achat.fournisseur

            if achat.type_paiement == 'partiel':
                # Paiement total, soustrayez le montant total HT du solde du fournisseur
                fournisseur.solde += achat.montant_total_ht

            fournisseur.save()

            # Mettre à jour la quantité en stock du produit
            produit = achat.produit
            produit.quantite_en_stock += achat.quantite
            produit.save()

            return redirect('liste_achats')
        
    else:
        achat_form = AchatForm()

    return render(request, 'achats/achat_form.html', {'achat_form': achat_form})


def liste_achats(request):
    achats = Achat.objects.all()
    return render(request, 'achats/liste_achats.html', {'achats': achats})

def regler_fournisseur(request):
    if request.method == 'POST':
        reglement_form = ReglementForm(request.POST)
        if reglement_form.is_valid():

            #achat = reglement.achat 

            #prix_produit = achat.montant_total_ht
            #reglement.prix_produit = prix_produit

            reglement = reglement_form.save(commit=False)
            reglement.achat.fournisseur.solde -= reglement.montant
            reglement.achat.fournisseur.save()
            reglement.save()
        return redirect('liste_reglements')
    else:
        reglement_form = ReglementForm()

    return render(request, 'achats/regler_fournisseur.html', {'reglement_form': reglement_form})


def liste_reglements(request):
    reglements = Reglement.objects.all()
    return render(request, 'achats/liste_reglements.html', {'reglements': reglements})


def apply_filters_achats(request, queryset):
    fournisseur = request.GET.get('fournisseur')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    filters = {}

    if fournisseur:
        filters['fournisseur'] = fournisseur

    if date_debut:
        filters['date_transfert__gte'] = date_debut

    if date_fin:
        filters['date_transfert__lte'] = date_fin

    return queryset.filter(**filters)

def fiche_journal_achats(request):
    achats = Achat.objects.all()
    fournisseurs = Fournisseur.objects.all()  

    achats_filtres = apply_filters_achats(request, achats)

    montant_total = sum(achat.montant_total_ht for achat in achats_filtres)

    return render(request, 'achats/fiche_journal_achats.html', {'achats': achats_filtres, 'montant_total': montant_total, 'fournisseurs': fournisseurs})

def modify_achat(request, achat_id):
    achat = get_object_or_404(Achat, id=achat_id)

    if request.method == 'POST':
        form = AchatForm(request.POST, instance=achat)
        if form.is_valid():
            form.save()
            return redirect('fiche_journal_achats')
    else:
        form = AchatForm(instance=achat)

    return render(request, 'achats/achats_edit.html', {'form': form, 'achat': achat})


def delete_achat(request, achat_id):
    achat = get_object_or_404(Achat, id=achat_id)

    if request.method == 'POST':
        achat.delete()
        return redirect('fiche_journal_achats')

    return render(request, 'achats/achats_delete.html', {'achat': achat})


def transfert_matiere(request):
    if request.method == 'POST':
        form = TransfertForm(request.POST)
        if form.is_valid():
            transfert = form.save(commit=False)

            # Vérifier si l'objet Transfert a une référence à un objet Achat
            if transfert.achat:
                transfert.cout_transfert = transfert.achat.prix_unitaire_ht * transfert.quantite
            else:
                # Si pas d'achat, vous pouvez définir le coût sur 0 ou gérer selon vos besoins
                transfert.cout_transfert = 0

            transfert.save()
            return redirect('fiche_journal_transferts')
    else:
        form = TransfertForm()

    return render(request, 'transferts/transfert_form.html', {'form': form})


def apply_filters_transferts(request, queryset):
    centre = request.GET.get('centre')
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    filters = {}

    if centre:
        filters['centre'] = centre

    if date_debut:
        filters['date_transfert__gte'] = date_debut

    if date_fin:
        filters['date_transfert__lte'] = date_fin

    return queryset.filter(**filters)

def fiche_journal_transferts(request):
    transferts = Transfert.objects.all()
    centres = Centre.objects.all()

    # Gérer la logique des filtres en utilisant la fonction apply_filters
    if request.method == 'GET':
        transferts = apply_filters_transferts(request, transferts)

    form = TransfertFilterForm(request.GET)

    return render(request, 'transferts/fiche_journal_transferts.html', {'transferts': transferts, 'form': form, 'centres': centres})

def vente_matiere(request):
    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            vente.montant_vente = vente.prix_unitaire_vente * vente.quantite

            # Récupérer le crédit du client sélectionné
            client_credit = Client.objects.get(pk=vente.client.id).credit

            if vente.type_paiement == 'partiel': 
                # Mettez à jour le crédit du client
                #montant_encaisse = vente.montant_encaisse or 0
                #reste_a_payer = vente.montant_vente - montant_encaisse
                vente.credit_client = vente.montant_vente + client_credit
                vente.save()

            return redirect('fiche_journal_ventes')
    else:
        form = VenteForm()

    return render(request, 'ventes/vente_form.html', {'form': form})

def get_client_credit(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        client = get_object_or_404(Client, pk=client_id)
        return JsonResponse({'credit': client.credit})

def fiche_journal_ventes(request):
    ventes = Vente.objects.all()

    if request.method == 'POST':
        form = VenteForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)

            # Gérer le paiement crédit des clients
            if vente.client.credit > 0:
                vente.client.credit -= vente.montant_encaisse
                vente.client.save()

            vente.save()

    else:
        form = VenteForm()

    return render(request, 'ventes/fiche_journal_ventes.html', {'ventes': ventes, 'form': form})

def modify_vente(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)

    if request.method == 'POST':
        form = VenteForm(request.POST, instance=vente)
        if form.is_valid():
            form.save()
            return redirect('fiche_journal_ventes')
    else:
        form = VenteForm(instance=vente)

    return render(request, 'ventes/vente_edit.html', {'form': form, 'vente': vente})

def delete_vente(request, vente_id):
    vente = get_object_or_404(Vente, id=vente_id)

    if request.method == 'POST':
        vente.delete()
        return redirect('fiche_journal_ventes')

    return render(request, 'ventes/vente_delete.html', {'vente': vente})

def apply_filters_produits(request, queryset):
    fournisseur_id = request.GET.get('fournisseur')
    date_achat_debut = request.GET.get('date_achat_debut')
    date_achat_fin = request.GET.get('date_achat_fin')
    produit_id = request.GET.get('produit')

    filters = {}

    if fournisseur_id:
        filters['achat__fournisseur__id'] = fournisseur_id

    if date_achat_debut:
        filters['achat__date_achat__gte'] = date_achat_debut

    if date_achat_fin:
        filters['achat__date_achat__lte'] = date_achat_fin

    if produit_id:
        filters['id'] = produit_id

    return queryset.filter(**filters)


import pdfkit
config = pdfkit.configuration(wkhtmltopdf=r"C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe")

def etat_stock(request):
    produits = Produit.objects.all()
    achats = Achat.objects.all()
    fournisseurs = Fournisseur.objects.all()

    form = FilterForm(request.GET)  # Crée une instance du formulaire avec les données de la requête

    if form.is_valid():
        produits_filtres = apply_filters_produits(request, produits)
        valeur_totale_stock = sum(achat.montant_total_ht for achat in Achat.objects.filter(produit__in=produits_filtres))
    else:
        produits_filtres = produits
        valeur_totale_stock = sum(achat.montant_total_ht for achat in Achat.objects.filter(produit__in=produits))

    context = {
        'form': form,
        'produits': produits,
        'produits_filtres': produits_filtres,
        'valeur_totale_stock': valeur_totale_stock,
        'achats' : achats,
        'fournisseurs': fournisseurs,
    }

    return render(request, 'stock/etat_stock.html', context)

def generate_pdf(request):
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('etat_stock')), False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etat_stock.pdf"'
    return response

    ##return render(request, 'stock/etat_stock.html', {'achats': achats, 'produits': produits, 'produits_filtres': produits_filtres, 'valeur_totale_stock': valeur_totale_stock, 'fournisseurs': fournisseurs, 'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Centre, Vente
from .forms import VenteForm  # Assurez-vous de créer un formulaire Django pour les ventes


def enregistrer_vente_centre(request, centre_id):
    centre = get_object_or_404(Centre, pk=centre_id)
    
    credit_client = 0  # Initialiser la variable credit_client à une valeur par défaut
    
    if request.method == 'POST':
        form = VenteForm(request.POST)
        
        if form.is_valid():
            vente = form.save(commit=False)
            
            # Définir le client associé à la vente
            vente.client = form.cleaned_data['client']
            
            # Calcul du montant total avant d'enregistrer la vente
            vente.montant_vente = vente.prix_unitaire_vente * vente.quantite
            
            # Indiquer le montant versé
            vente.montant_encaisse = form.cleaned_data['montant_encaisse']
            
            vente.save()
            # Logique supplémentaire si nécessaire...
            return redirect('CentreList')  # Redirection vers CentreList
    
    else:
        form = VenteForm()

    
    return render(request, 'activiteCentre/enregistrer_vente_centre.html', {'form': form, 'centre': centre, 'credit_client': credit_client})

def paiement_credit_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    if request.method == 'POST':
        form = PaiementCreditForm(request.POST)
        if form.is_valid():
            montant = form.cleaned_data['montant']
            client.credit -= montant
            client.save()
            return redirect('list_achats')  # Redirigez vers la page appropriée
    else:
        form = PaiementCreditForm()
    return render(request, 'clients/paiement_credit.html', {'form': form, 'client': client})




def details_activite_centre(request, centre_id):
    # Récupérez le centre spécifique en fonction de l'ID
    centre = get_object_or_404(Centre, id=centre_id)
    
    # Récupérez toutes les ventes associées à ce centre
    ventes = Vente.objects.all()  # Vous obtenez toutes les ventes ici
    
    # Récupérez tous les règlements clients associés à ce centre
    reglements = ReglementClient.objects.all()  # Vous obtenez tous les règlements ici
    
    return render(request, 'activiteCentre/details_activite_centre.html', {'ventes': ventes, 'reglements': reglements, 'centre': centre})


def regler_client(request):
    if request.method == 'POST':
        reglementVente_form = ReglementVenteForm(request.POST)
        if reglementVente_form.is_valid():

            #achat = reglement.achat 

            #prix_produit = achat.montant_total_ht
            #reglement.prix_produit = prix_produit

            reglement = reglementVente_form.save(commit=False)
            reglement.vente.client.credit -= reglement.montant
            reglement.vente.client.save()
            reglement.save()
        return redirect('liste_reglements')
    else:
        reglementVente_form = ReglementVenteForm()

    return render(request, 'ventes/regler_client.html', {'reglementVente_form': reglementVente_form})


def details_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)

    # Logique pour récupérer les absences et les avances récentes (à ajuster selon vos besoins)
    absences_recentes = Absence.objects.filter(employe=employe, date_absence__gte=timezone.now() - timezone.timedelta(days=30))
    avances_recentes = Avance.objects.filter(employe=employe, date_demande__gte=timezone.now() - timezone.timedelta(days=30))

    # Calcul automatique du salaire à la fin de chaque mois
    mois_actuel = timezone.now().month
    jours_du_mois = timezone.now().replace(month=mois_actuel + 1, day=1) - timezone.now().replace(day=1)
    
    # Assurez-vous que votre modèle Employe a un champ 'salaire_jour'
    salaire_total = Employe.objects.annotate(salaire_mois=Sum('salaire_jour') * 30).filter(id=employe_id, isDeleted=False)

    # Logique pour passer ces données à votre template
    context = {
        'employe': employe,
        'absences_recentes': absences_recentes,
        'avances_recentes': avances_recentes,
        'salaire_total': salaire_total,
    }
    
    return render(request, 'employes/EmpDetails.html', context)



def ajouter_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save(commit=False)
            
            # Récupérer l'employé associé à l'absence
            employe = absence.employe

            # Incrémenter le nombre d'absences de l'employé
            employe.nombreAbscence = employe.nombreAbscence + 1 if employe.nombreAbscence else 1

            # Sauvegarder l'employé mis à jour
            employe.save()

            # Sauvegarder l'absence
            absence.save()

            return redirect('EmpList')
    else:
        form = AbsenceForm()

    context = {
        'form': form,
    }
    return render(request, 'employes/ajouter_absence.html', context)




def demander_avance(request):
    if request.method == 'POST':
        form = AvanceForm(request.POST)
        if form.is_valid():
            avance = form.save(commit=False)
            employe = avance.employe
            employe.demandeAvance = True 

            avance.save()
            return redirect('EmpList')
    else:
        form = AvanceForm()

    context = {'form': form}
    return render(request, 'employes/EmpAvance.html', context)

