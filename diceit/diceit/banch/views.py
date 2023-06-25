from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import random
from braces.views import GroupRequiredMixin
from store.models import Dice
import uuid
import re
from django.contrib.auth.models import User
from django import forms


# Create your views here.
def has_group(user):
    return user.groups.filter(name="artigiani").exists()

@user_passes_test(has_group)
def banch(request):
    dice_faces = ('⚀',
                  "⚁",
                  "⚂",
                  "⚃",
                  "⚄",
                  "⚅",
                  )
    
    dice1 =  random.choice(dice_faces)
    dice2 =  random.choice(dice_faces)
    ctx = {
        'card1' : dice1,
        'card2' : dice2,
        'lucky' : (dice1 == dice2),
    }
    return render(request, template_name='banch/banch.html', context=ctx)

'''Usare un model form per un immagine è consigliato se essa è salvata nel db, invece questo progetto risolve il dodumento
statico tramite il codice del diceset, quindi procedo in questo caso con una FBV'''
class FileUploadForm(forms.Form):
    file = forms.FileField()

@user_passes_test(has_group)
def add_set(request):
    #genero un codice resistente alle collisioni

    if request.method == "POST":
        code = request.POST['code']
        creator = request.POST['creator']
        creator = User.objects.get(username__iexact=creator)
        #campo "pericoloso, rimuoviamo i caratteri speciali"
        name = request.POST['name']
        pattern = r'[^a-zA-Z0-9\s]'  # Matches any character that is not alphanumeric, whitespace, hyphen, or underscore
        name = re.sub(pattern, '', name)
        #questo deve essere un intero
        num_pice = request.POST['nump']
        num_pice = int(num_pice)
        color = request.POST['color']
        #altro campo un po pericoloso 
        descr = request.POST['descr']
        descr = re.sub(pattern, '', descr)
        avail = request.POST['avail']
        if avail == "Y":
            avail = True
        else:
            avail = False
        #questo è da trasformare in float
        price = request.POST['price']
        price = float(price)

        #caricamento immagine
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            print(type(uploaded_file), uploaded_file)
        else:
            print("funziona")
        
        
        #se ho caricato un immagine, allora la salvo, altrimenti i vari template caricheranno il default 
        #creazione del nuovo dado
        d = Dice()
        d.code = code
        d.name = name
        d.number_of_pices = num_pice
        d.primary_color = color
        d.description = descr
        d.available = avail
        d.price = price
        d.seller = creator
        #d.save()
        ctx = {
            'dice_code' : d.code,
        }
    else:
        ctx = {
            'code' : uuid.uuid4(),
            'form' : FileUploadForm(),
        }
    return render(request, template_name='banch/create_set.html', context=ctx)