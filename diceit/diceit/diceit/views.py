from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from store.models import Purchase, Dice
from . import rater

def home(request):

    # Check if the user belongs to the "admin" group
    if request.user.groups.filter(name='artigiani').exists():
        ctx = {'artigiano' : True}
    else:
        # User is not in the "admin" group
        # Perform actions for non-admin users
        ctx = {'artigiano' : False}

    return render(request, template_name='home.html', context=ctx)

@login_required
def diventa_artigiano(request):

    if request.method == "POST":
        user = request.user
        Group.objects.get_or_create(name='artigiani')
        artigiani = Group.objects.get(name='artigiani')
        artigiani.user_set.add(user)
        ctx = { 'registrato' : True}
    else:
        ctx = { 'registrato' : False}

    return render(request, template_name='diventa_artigiano.html', context=ctx)

def has_group(user):
    return user.is_superuser

'''Questa view deve essere raggiungibile solo da un superuser, e ha lo scopo di creare e/o aggiornare il reccomandation system.
L'operazione prevede di raccogliere ogni utente, e i suoi acquisti, e per ogni set di dadi che ha comprato verrà creato uno score
basato sul numero di volte che ha comprato quel set.
Queste informazioni andranno su un file che sarà letto dal motore di raccomandazione, creando un oggetto accessibile da altre views.
Lo scopo di questa view è raccogliere le informazioni affinchè ciò sia possibile.
Il sistema è memory based (si basa su altri acquisti fatti da utenti) e user based: cercherà di predirre la probabilità di un acquisti.
In base alla similarità tra gli utenti. '''
@user_passes_test(has_group)
def update_reccomendation(request):
    
    rater.set_up_reccomendation_file()

    return render(request, template_name='update_rec.html')