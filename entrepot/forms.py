from django import forms
from .models import Produit, Client, Fournisseur, Centre, Employe, Achat, Reglement, ReglementClient, Transfert, Vente

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['code', 'designation']  

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['code', 'nom' , 'prenom', 'adresse', 'telephone', 'credit'] 

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['code', 'nom' , 'prenom', 'adresse', 'telephone', 'solde'] 

class CentreForm(forms.ModelForm):
    class Meta:
        model = Centre
        fields = ['code', 'designation']  

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['code', 'nom' , 'prenom', 'adresse', 'telephone', 'salaire_jour', 'centre']  


class AchatForm(forms.ModelForm):
    class Meta:
        model = Achat
        fields = ['fournisseur', 'produit', 'quantite', 'prix_unitaire_ht', 'date_achat' ,'type_paiement']

class ReglementForm(forms.ModelForm):
    class Meta:
        model = Reglement
        fields = ['fournisseur', 'montant', 'date_reglement']


class FicheJournalAchatsFilterForm(forms.Form):
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all(), required=False, empty_label="Tous les fournisseurs")    



class TransfertForm(forms.ModelForm):
    class Meta:
        model = Transfert
        fields = ['centre', 'produit', 'quantite', 'date_transfert']


class TransfertFilterForm(forms.Form):
    centre = forms.ModelChoiceField(queryset=Centre.objects.all(), required=False, label='Centre')
    date_debut = forms.DateField(required=False, label='Date de début')
    date_fin = forms.DateField(required=False, label='Date de fin')



class VenteForm(forms.ModelForm):
    credit_client = forms.DecimalField(
        label='Crédit du client',
        widget=forms.NumberInput(attrs={'readonly': 'readonly', 'id': 'id_credit_client'}),
    )

    class Meta:
        model = Vente
        fields = ['client', 'produit', 'quantite', 'prix_unitaire_vente', 'date_vente', 'montant_encaisse']
        



class FilterForm(forms.Form):
    fournisseur = forms.ModelChoiceField(queryset=Fournisseur.objects.all(), required=False, label='Fournisseur')
    ##date_achat_debut = forms.DateField(required=False, label='Date d\'achat (fin)')
    date_achat_debut = forms.DateField(
        required=False,
        label='Date d\'achat (debut)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    date_achat_fin = forms.DateField(
        required=False,
        label='Date d\'achat (fin)',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    produit = forms.ModelChoiceField(queryset=Produit.objects.all(), required=False, label='Produit')



class AjustementStockForm(forms.Form):
    produit = forms.ModelChoiceField(queryset=Produit.objects.all(), label='Produit')
    quantite_ajustee = forms.IntegerField(label='Quantité ajustée')
    motif = forms.CharField(widget=forms.Textarea, label='Motif de l\'ajustement')


class PaiementCreditForm(forms.Form):
    montant = forms.DecimalField(label='Montant du Paiement', max_digits=10, decimal_places=2)

    def clean_montant(self):
        montant = self.cleaned_data['montant']
        # Vous pouvez ajouter ici une logique de validation supplémentaire si nécessaire
        if montant <= 0:
            raise forms.ValidationError("Le montant doit être positif.")
        return montant


class ReglementClientForm(forms.ModelForm):
    class Meta:
        model = ReglementClient
        fields = ['client', 'montant_reglement']