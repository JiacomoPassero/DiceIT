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
    '''
    #devo creare una entry per ogni coppia dado - utente per permettere al rater di lavorare
    dadi = Dice.objects.all()
    user = User.objects.all()
    purchases = Purchase.objects.all()
    #inizializzo il dizionario
    rating = {}
    for u in user:
        for d in dadi:
            key = u.username + " " +d.code
            rating[key] = 0 
    
    #aggiorno con chi ha modificato il valore
    for p in purchases:
        codice_dado = p.dice_set.code
        nome_utente = p.buyer.username
        key =  nome_utente + " " + codice_dado
        rating[key] = rating[key] + p.amount_of_sets


    massimo = max(rating.values())
    #ora ho le informazioni necessarie per costruire il rating system
    #le salvo sul file in formato 'item' 'user' 'rating', separati da spazio
    f = open("diceit/ratings.txt", "w")
    for key, val in rating.items():
        #print(key,val)
        foo = (val*10)/massimo#aggiustamento scala per il rater
        foo = int(foo)
        #il rater non può lavorare con valori a 0
        if foo == 0:
            foo = 1
        f.write(key+" "+str(foo)+'\n')

    f.close()'''
    rater.set_up_reccomendation_file()

    return render(request, template_name='update_rec.html')