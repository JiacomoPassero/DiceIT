from django.shortcuts import render
from store.models import User, Dice


# Create your views here.
def store(request):

    #dices = Dice.objects.all()
    
    if request.method == "POST":
        colore = request.POST['color']
        nome= request.POST['name']
        #print("colore",colore," ",type(colore))
        #print("nome",nome," ",type(nome))
        if colore != "none" and nome != "":
            dices= Dice.objects.filter(primary_color__exact=colore,name__iexact=nome)
        else:
            if colore != "none":
                dices = Dice.objects.filter(primary_color__exact=colore)
            if  nome != "":
                dices = Dice.objects.filter(name__iexact=nome)        
    
        if nome == "":
            if colore == "none":
                #premuto search senza parametri
                dices = Dice.objects.all()

    else:
        dices = Dice.objects.all()

    if not dices:
        vuoto = True
    else:
        vuoto = False

    ctx = { 
            'dices' :   dices,
            'vuoto' : vuoto
        }
    #Stile tabella Masonry, il dislivello è voluto
    return render(request, template_name='store/store.html', context=ctx)