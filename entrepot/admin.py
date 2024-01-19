from django.contrib import admin

from .models import Produit
admin.site.register(Produit)


from .models import Client
admin.site.register(Client)


from .models import Fournisseur
admin.site.register(Fournisseur)

from .models import Centre
admin.site.register(Centre)

from .models import Employe
admin.site.register(Employe)

from .models import Vente
admin.site.register(Vente)

from .models import Achat
admin.site.register(Achat)

from .models import Reglement
admin.site.register(Reglement)

from .models import Avance
admin.site.register(Avance)