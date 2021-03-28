#encoding:utf-8

from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator




class Skin_Lesion(models.Model):
   id =   models.AutoField(primary_key=True)
   creation_date   =   models.TimeField(auto_now_add=True)
   description = models.CharField(max_length=200)
   image = models.ImageField(upload_to = 'image')
   



class Dossier(models.Model):
    id              =   models.AutoField(primary_key=True)
    titulo          =   models.CharField(max_length=100)
    creation_date   =   models.TimeField(auto_now_add=True)
    skin_lesion     =   models.ManyToManyField(Skin_Lesion)


    def __str__(self):
        return self.titulo

class Custom_User(models.Model):

    user_id         =   models.AutoField(primary_key=True)
    user_name       =   models.TextField(max_length=10)
    user_pass       =   models.TextField(max_length=10)
    creation_date   =   models.TimeField(auto_now_add=True)
    date_of_birth   =   models.DateField()
    active = models.BooleanField()
    dossier         =   models.ManyToManyField(Dossier,blank=True)

