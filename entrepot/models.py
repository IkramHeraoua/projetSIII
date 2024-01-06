from django.db import models

# Create your models here.
class Produit(models.Model):
    code = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    quantite_en_stock = models.PositiveIntegerField(default=0)
    isDeleted = models.BooleanField(default= False )
    def __str__(self):
        return str(self.code)

   
class Client(models.Model):
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    credit = models.DecimalField(max_digits=10, decimal_places=2)
    isDeleted = models.BooleanField(default= False )
    def __str__(self):
        return str(self.nom)

    

class Fournisseur(models.Model):
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    isDeleted = models.BooleanField(default= False )
    def __str__(self):
        return str(self.nom)
    

class Centre(models.Model):
    code = models.CharField(max_length=20)
    designation = models.CharField(max_length=100)
    isDeleted = models.BooleanField(default= False )
    def __str__(self):
        return str(self.code)
   

class Employe(models.Model):
    code = models.CharField(max_length=20)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=15)
    salaire_jour = models.DecimalField(max_digits=10, decimal_places=2)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    isDeleted = models.BooleanField(default= False )
    def __str__(self):
        return str(self.nom)
    
    

class Achat(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2)
    date_achat = models.DateField()
    montant_total_ht = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    TYPE_PAIEMENT_CHOICES = (
        ('total', 'Paiement total'),
        ('partiel', 'Paiement partiel'),
    )
    type_paiement = models.CharField(
        max_length=15,
        choices=TYPE_PAIEMENT_CHOICES,
        default='total', 
    )
    #montant_verse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    


class Reglement(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_reglement = models.DateField()
    def __str__(self):
        return f"Règlement de {self.montant} pour {self.fournisseur} le {self.date_reglement}"
    


class Transfert(models.Model):
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    achat = models.ForeignKey(Achat, on_delete=models.CASCADE, blank=True, null=True)
    quantite = models.PositiveIntegerField()
    date_transfert = models.DateField()
    cout_transfert = models.DecimalField(max_digits=10, decimal_places=2, editable=False)


class Vente(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE, null = True)
    quantite = models.PositiveIntegerField()
    prix_unitaire_vente = models.DecimalField(max_digits=10, decimal_places=2)
    montant_vente = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    date_vente = models.DateField()
    montant_encaisse = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        self.montant_vente = self.quantite * self.prix_unitaire_vente
        super(Vente, self).save(*args, **kwargs)
        if self.montant_encaisse < self.montant_vente:
            self.client.credit -= self.montant_encaisse
            self.client.save()
                 

class ActiviteCentre(models.Model):
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)
    date_activite = models.DateField()
    # Ajoutez d'autres champs spécifiques à l'activité du centre (par exemple, le total des ventes, le total des transferts, etc.)
    total_ventes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_transferts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # autres champs nécessaires...



class ReglementClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    montant_reglement = models.DecimalField(max_digits=10, decimal_places=2)
    date_reglement = models.DateField()