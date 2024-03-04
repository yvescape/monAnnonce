from django.contrib import admin
from .models import (Categorie,Announce,Contact,Commentaire)
# Register your models here.

admin.site.register(Categorie)
admin.site.register(Announce)
admin.site.register(Commentaire)
admin.site.register(Contact)
