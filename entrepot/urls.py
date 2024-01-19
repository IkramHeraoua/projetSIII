from django.urls import path 
from . import views
urlpatterns = [
    path('base/',views.base_view, name='base'),

    #produit
    path('ProdList/',views.list_produits, name='ProdList'),
    path('ProdEdit/<int:produit_id>/',views.update_produit, name='ProdEdit'),
    path('ProdDelete/<int:produit_id>/',views.delete_produit, name='ProdDelete'),
    path('ProdCreate/',views.create_produit, name='ProdCreate'),

    #client
    path('ClientList/',views.list_clients, name='ClientList'),
    path('ClientEdit/<int:client_id>/',views.update_client, name='ClientEdit'),
    path('ClientDelete/<int:client_id>/',views.delete_client, name='ClientDelete'),
    path('ClientCreate/',views.create_client, name='ClientCreate'),

    #centre
    path('CentreList/',views.list_centres, name='CentreList'),
    path('CentreEdit/<int:centre_id>/',views.update_centre, name='CentreEdit'),
    path('CentreDelete/<int:centre_id>/',views.delete_centre, name='CentreDelete'),
    path('CentreCreate/',views.create_centre, name='CentreCreate'),

    #employe
    path('EmpList/',views.list_employes, name='EmpList'),
    path('EmpEdit/<int:employe_id>/',views.update_employe, name='EmpEdit'),
    path('EmpDelete/<int:employe_id>/',views.delete_employe, name='EmpDelete'),
    path('EmpDetails/<int:employe_id>/',views.details_employe, name='EmpDetails'),
    path('EmpCreate/',views.create_employe, name='EmpCreate'),
    path('ajouter_absence/', views.ajouter_absence, name='ajouter_absence'),
    path('EmpAvance/', views.demander_avance, name='EmpAvance'),


     #fournisseur
    path('FourList/',views.list_fournisseurs, name='FourList'),
    path('FourEdit/<int:fournisseur_id>/',views.update_fournisseur, name='FourEdit'),
    path('FourDelete/<int:fournisseur_id>/',views.delete_fournisseur, name='FourDelete'),
    path('FourCreate/',views.create_fournisseur, name='FourCreate'),


    #achats
    path('acheter_matiere/', views.acheter_matiere, name='acheter_matiere'),
    path('liste_achats/', views.liste_achats, name='liste_achats'),
    path('regler_fournisseur/', views.regler_fournisseur, name='regler_fournisseur'),
    path('liste_reglements/', views.liste_reglements, name='liste_reglements'),
    path('fiche_journal_achats/', views.fiche_journal_achats, name='fiche_journal_achats'),
    path('modify_achat/<int:achat_id>/', views.modify_achat, name='modify_achat'),
    path('delete_achat/<int:achat_id>/', views.delete_achat, name='delete_achat'),


    #transferts
    path('transfert_matiere/', views.transfert_matiere, name='transfert_matiere'),
    path('fiche_journal_transferts/', views.fiche_journal_transferts, name='fiche_journal_transferts'),

    #ventes
    path('vente_matiere/', views.vente_matiere, name='vente_matiere'),
    path('fiche_journal_ventes/', views.fiche_journal_ventes, name='fiche_journal_ventes'),
    path('modify_vente/<int:vente_id>/', views.modify_vente, name='modify_vente'),
    path('delete_vente/<int:vente_id>/', views.delete_vente, name='delete_vente'),
    path('get_client_credit/', views.get_client_credit, name='get_client_credit'),
     path('regler_client/', views.regler_client, name='regler_client'),



    path('etat_stock/', views.etat_stock, name='etat_stock'),
    path('etat_stock_pdf/', views.generate_pdf, name='etat_stock_pdf'),



    path('enregistrer_vente_centre/<int:centre_id>', views.enregistrer_vente_centre , name='enregistrer_vente_centre'),
    path('paiement_credit_client/', views.paiement_credit_client , name='paiement_credit_client'),
    path('details_activite_centre/<int:centre_id>/', views.details_activite_centre, name='details_activite_centre'),

    

 ]