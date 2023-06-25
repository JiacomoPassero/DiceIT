from typing import Any, Dict
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import random
from braces.views import GroupRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from store.models import Dice
from django import forms
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
import uuid


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
@user_passes_test(has_group)
def add_set(request):
    #genero un codice resistente alle collisioni
    ctx = {
        'code' : uuid.uuid4()
    }
    return render(request, template_name='banch/create_set.html', context=ctx)