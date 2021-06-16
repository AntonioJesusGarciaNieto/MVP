#encoding:utf-8

#Imports de Django
from main.models import Skin_Lesion
from django.shortcuts import render, HttpResponse,redirect
from django.template import RequestContext
from django.http.response import HttpResponseRedirect
from django.conf import settings
import re, os, shutil

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2


print(tf.__version__)




from django.shortcuts import render
from .models import *
from .forms import *
from django.http import HttpResponseRedirect


###########################################################
#                       Loads                             #
###########################################################
def dossieres(request):

    user_name = request.session['user_name']
    user_pass = request.session['user_pass']

    user = Custom_User.objects.get(user_name=user_name,user_pass=user_pass)

    dossiers = user.dossier.all()

    dossiers_and_count = []
    for doss in dossiers:
        img_number = doss.skin_lesion.count()
        dossiers_and_count.append((doss,img_number))


    is_active = request.session.get("user_active",False)
    return render(request,'dossiers.html',{'is_active':is_active,'dossiers_and_count':dossiers_and_count})

def index(request):


    is_active = request.session.get("user_active",False)

    return render(request,'index.html',{'is_active':is_active})

def logout(request):
    mensaje = "Bienvenido, para disfrutar de la funcionalidad debe ser un usuario loggeado"
    if request.method == 'POST' and request.POST.get("Res")=="Aceptar":
        
        user_name = request.session['user_name']
        user_pass = request.session['user_pass']
        print(user_name)
        user = Custom_User.objects.get(user_name=user_name,user_pass=user_pass)
        user.active = False
        user.save()

        request.session['user_active'] = False

        is_active = request.session.get("user_active",False)
        print(is_active)

        request.session.modified = True

        is_active = False
        print(is_active)

        return render(request,'index.html',{'is_active':is_active})

    is_active = request.session.get("user_active",False)
        
    return render(request,'logout.html',{'is_active':is_active})

def new_dossier(request):
    if request.method == 'POST':

        user_name = request.session['user_name']
        user_pass = request.session['user_pass']

        
        if request.FILES.get("image"):
            img = Skin_Lesion()
            img.image = request.FILES.get("image")
            img.name = request.POST.get("name")
            img.save()

            doss = Dossier()
            doss.titulo = request.POST.get("doss_name")
            doss.save()
            doss.skin_lesion.add(img)
            doss.save()

            user = Custom_User.objects.get(user_name=user_name,user_pass=user_pass)
            user.dossier.add(doss)

            request.session.modified = True
            
            user = Custom_User.objects.get(user_name=user_name,user_pass=user_pass)

            dossiers = user.dossier.all()

            dossiers_and_count = []
            for doss in dossiers:
                img_number = doss.skin_lesion.count()
                dossiers_and_count.append((doss,img_number))

            is_active = request.session.get("user_active",False)
            return render(request,'dossiers.html',{'is_active':is_active,'dossiers_and_count':dossiers_and_count})

    is_active = request.session.get("user_active",False)
        

    return render(request,'new_dossier.html',{'is_active':is_active})

def login(request):
    mensaje = "Bienvenido, para disfrutar de la funcionalidad debe ser un usuario loggeado"
    if request.method == 'POST':
        user_name=request.POST.get("user_name")
        user_pass=request.POST.get("user_pass")
        try:
            user = Custom_User.objects.get(user_name=user_name,user_pass=user_pass)
            user.active = True
            user.save()
            request.session['user_name'] = user_name
            request.session['user_pass'] = user_pass
            request.session['user_active'] = True

            print(request.session['user_active'])
            request.session.modified = True
        except:
            mensaje = "Usuario o contraseña incorrectos"

        
        is_active = request.session.get("user_active",False)

    is_active = request.session.get("user_active",False)
        

    return render(request,'login.html',{'mensaje': mensaje,'is_active':is_active})

def registro(request):
    mensaje = "Rellena los campos y da click en aceptar : )"
    if request.method == 'POST':
        user_name=request.POST.get("user_name")
        user_pass=request.POST.get("user_pass")
        date_of_birth=request.POST.get("date_of_birth")
        if True:
            print("----"+str(user_name)+str(user_pass)+str(date_of_birth))
            Custom_User.objects.create(user_name=user_name,user_pass=user_pass,active=True,date_of_birth=date_of_birth)
            request.session['user_name'] = user_name
            request.session['user_pass'] = user_pass
            request.session['user_active'] = True
            request.session.modified = True

        
        is_active = request.session.get("user_active",False)

    is_active = request.session.get("user_active",False)
        

    return render(request,'login.html',{'mensaje': mensaje,'is_active':is_active,'is_regist':True})

###########################################################
#                        Otros                            #
###########################################################

def show_dossier(request):
    if request.method == 'POST':
        dossier_id=request.POST.get("dossier_id")
        dossier = Dossier.objects.get(id=dossier_id)
        dossier_title = dossier.titulo
        dossier_id = dossier.id

        skinsLesions = dossier.skin_lesion.all()
        print(skinsLesions[0].id)
    
    is_active = request.session.get("user_active",False)
    return render(request,'show_dossier.html',{'skinsLesions': skinsLesions,'dossier_title':dossier_title,"dossier_id":dossier_id,'is_active':is_active})
        
def analyze(request):
    if request.method == 'POST' :

        id = request.POST.get("sl_id")
        img = Skin_Lesion.objects.get(id=id).image

        path_model = 'data/model.h5'
        new_model = tf.keras.models.load_model(path_model)
        img = np.array(img)
        url = "../media/"+str(img)
        img = cv2.imread("media/"+str(img))
        img = cv2.resize(img, (50, 50))
        img = img.astype(np.float32) / 255.

        img = img[None,...]
        res = new_model.predict(img)

        lista = res.tolist()
        dic1 = {}

        lesion_type_dict = {
            0: 'Melanocytic nevi',
            1: 'Melanoma',
            2: 'Benign keratosis ',
            3: 'Basal cell carcinoma',
            4: 'Actinic keratoses',
            5: 'Vascular lesions',
            6: 'Dermatofibroma'
        }

        for index in range(len(lista[0])):
            key = lesion_type_dict[index]
            dic1[key] = lista[0][index]

        res = []
        k = list(dic1.keys())
        v = list(dic1.values())
        for index in range(len(lista[0])):
            res.append((k[index],v[index]))

        is_active = request.session.get("user_active",False)    
    
        return render(request,'show_analytics.html',{'res': res,'url':url, 'ready':True,"is_active":is_active})

    else:
        is_active = request.session.get("user_active",False)
        return render(request,'README.html',{"is_active":is_active})        

def readme(request):
    if request.method == 'POST' :
        img = Skin_Lesion()
        img.image = request.FILES.get("image")
        img.name = request.POST.get("name")
        global COUNT
        img.id = COUNT
        img.save()

 
        

        img = Skin_Lesion.objects.get(id=COUNT)
        COUNT = COUNT + 1
        img = img.image
        path_model = 'data/model.h5'
        new_model = tf.keras.models.load_model(path_model)
        img = np.array(img)
        url = "../media/"+str(img)
        img = cv2.imread("media/"+str(img))
        img = cv2.resize(img, (50, 50))
        img = img.astype(np.float32) / 255.

        img = img[None,...]
        res = new_model.predict(img)

        lista = res.tolist()
        dic1 = {}

        lesion_type_dict = {
            0: 'Melanocytic nevi',
            1: 'Melanoma',
            2: 'Benign keratosis ',
            3: 'Basal cell carcinoma',
            4: 'Actinic keratoses',
            5: 'Vascular lesions',
            6: 'Dermatofibroma'
        }

        for index in range(len(lista[0])):
            key = lesion_type_dict[index]
            dic1[key] = lista[0][index]

        res = []
        k = list(dic1.keys())
        v = list(dic1.values())
        for index in range(len(lista[0])):
            res.append((k[index],v[index]))

        is_active = request.session.get("user_active",False)    
    
        return render(request,'README.html',{'res': res,'url':url, 'ready':True,"is_active":is_active})

    else:
        is_active = request.session.get("user_active",False)
        return render(request,'README.html',{"is_active":is_active})

def new_skin_lesion(request):

    if request.method == 'POST':
        img = Skin_Lesion()
        img.image = request.FILES.get("image")
        img.name = request.POST.get("name")
        img.save()
        d_id = request.POST.get("dossier_id")
        print("Print----------------------"+str(d_id))
        doss = Dossier.objects.get(id=d_id)
        doss.skin_lesion.add(img)
        doss.save() 

        request.session.modified = True

        img = img.image
        path_model = 'data/model.h5'
        new_model = tf.keras.models.load_model(path_model)
        img = np.array(img)
        url = "../media/"+str(img)
        img = cv2.imread("media/"+str(img))
        img = cv2.resize(img, (50, 50))
        img = img.astype(np.float32) / 255.

        img = img[None,...]
        res = new_model.predict(img)

        lista = res.tolist()
        dic1 = {}

        lesion_type_dict = {
            0: 'Melanocytic nevi',
            1: 'Melanoma',
            2: 'Benign keratosis ',
            3: 'Basal cell carcinoma',
            4: 'Actinic keratoses',
            5: 'Vascular lesions',
            6: 'Dermatofibroma'
        }

        for index in range(len(lista[0])):
            key = lesion_type_dict[index]
            dic1[key] = lista[0][index]

        res = []
        k = list(dic1.keys())
        v = list(dic1.values())
        for index in range(len(lista[0])):
            res.append((k[index],v[index]))

        is_active = request.session.get("user_active",False)    
    
        return render(request,'new_skin_lesion.html',{'res': res,'url':url, 'ready':True,"is_active":is_active})

    else:
        dossier_id = request.GET.get("dossier_id")
        print("++++++++++++++++++++++++++++"+str(dossier_id))
        is_active = request.session.get("user_active",False)
        
    return render(request,'new_skin_lesion.html',{"is_active":is_active,"dossier_id":dossier_id})