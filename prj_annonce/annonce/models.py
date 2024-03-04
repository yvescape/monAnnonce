from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length = 150) 
    description = models.TextField()

# standards
    status = models.BooleanField(default= True)
    date_add = models.DateTimeField(auto_now = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return self.nom


class Announce(models.Model) :
    titre = models.CharField(max_length = 150)
    image = models.ImageField(upload_to = "annouce/images")
    video = models.FileField(upload_to="annouce/videos", null=True)
    contenu = models.TextField()
    categorie = models.ForeignKey(Categorie,on_delete=models.CASCADE,related_name="annonce")
    autor = models.ForeignKey(User,on_delete=models.CASCADE,related_name="annonce")

    #standards
    status = models.BooleanField(default= False)
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.titre}({self.status})"
    

class Commentaire(models.Model):
    autor = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commentaire")
    announce_com = models.ForeignKey(Announce,on_delete=models.CASCADE,related_name="commentaire")
    commantaire = models.TextField()

    #standards
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return f"{self.autor.get_username()}"
    

class Contact(models.Model) :
    name = models.CharField(max_length = 150)
    email = models.CharField(max_length = 150)
    sujet = models.CharField(max_length = 150)
    contenu = models.TextField()

    #standards
    date_add = models.DateTimeField(auto_now_add = True)
    date_update =models.DateTimeField(auto_now = True)
    def __str__(self) :
        return self.sujet