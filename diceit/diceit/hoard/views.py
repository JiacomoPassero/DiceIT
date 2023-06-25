from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from store.models import Purchase, Dice
from django.contrib.auth.models import User
from django.db.models import Sum


# Create your views here.
@login_required
def hoard(request):
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
    
    return render(request, template_name='hoard/hoard.html', context=ctx)

@login_required
def show_hoard(request,user):
    #prendo l'attuale user come oggetto del db, per poterlo confrontare
    proprietario = User.objects.get(username__iexact=user)
    acquisti = Purchase.objects.filter(buyer__exact=proprietario)

    acquisti = acquisti.order_by('-date')
    ctx = {
        'acquisti' : acquisti,
        'numset' : acquisti.count(),
    }
    return render(request, template_name='hoard/show_hoard.html', context=ctx)

"Funzione di supporto per ordinamento collezionisti"
def returnSet(e):
    return e["num_set"]

"Funzione di conversione renking"
def ranking(num):
    if num < 10:
        rank = "Avarage Collector"
    elif num < 20:
        rank = "Dice enjoyer"
    elif num < 50:
        rank = "Dice Goblin"
    elif num < 100:
        rank = "Dice Dragon"
    else:
        rank = "Dice Demon"

    return rank

@login_required
def explore_hoards(request):
    tup = []

    collezionisti = User.objects.all()
    #Per ogni user, prendo la somma dei dadi comprati, e se non è none, allora procedo ad elaborarla
    for c in collezionisti:
        set_comprati = Purchase.objects.filter(buyer__exact=c)
        #nota, questo sotto restituisce comunque un dizionario, con un solo elemento
        set_comprati = set_comprati.aggregate(Sum('amount_of_sets'))
        set_comprati = set_comprati['amount_of_sets__sum']
            
        #se è none, allora non ci sono set comprati
        if set_comprati != None:
            col = {
                'user' : c,
                'num_set' : set_comprati,
                'rank' : ranking(set_comprati),
            }
            tup.append(col)

    tup.sort(reverse=True,key=returnSet)
    #l'utente che ha comprato più dadi è il Dice Emperor
    tup[0]["rank"] = "The Dice Emperor"
    
    #se sono arrivato tramite post, ci sono, o potrebbero essere filtri da applicare
    if request.method == "POST":
        name = request.POST['name']
        min= request.POST['min']
        max= request.POST['max']
        #dato che ho già la classifica con i rank già fatti, mi limito ad applicare
        #dei filtri in sequenza, partendo dal nome utente
        if name != "":
            tup = [t for t in tup if t['user'].username == name]
        #numero minimo di dadi richiesti
        if min != "":
            min = int(min)
            tup = [t for t in tup if t['num_set'] >= min]
        #numero massimo di dadi richiesti
        if max != "":
            max = int(max)
            tup = [t for t in tup if t['num_set'] <= max]

    
    ctx = {
        'collezionisti' : tup,
    }

    
    return render(request, template_name='hoard/explore_hoards.html', context=ctx)