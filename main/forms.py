#encoding:utf-8
from django import forms
from django.shortcuts import render
from .models import *



class UsuarioBusquedaForm(forms.Form):
    idUsuario = forms.CharField(label="idUsuario", widget=forms.Textarea(), required=True)
    
#class PeliculaBusquedaYearForm(forms.Form):
#    year = forms.IntegerField(label="Año de publicación", widget=forms.TextInput, required=True)