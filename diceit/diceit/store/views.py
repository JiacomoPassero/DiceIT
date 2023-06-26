from django.shortcuts import render
from store.models import Dice, Purchase
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User

from diceit import settings

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
        for d in dices:
            print (d.image)

    if not dices:
        vuoto = True
    else:
        vuoto = False

    ctx = { 
            'dices' :   dices,
            'vuoto' : vuoto,
            'MEDIA_URL' : settings.MEDIA_URL
        }
    #Stile tabella Masonry, il dislivello è voluto
    return render(request, template_name='store/store.html', context=ctx)

class UserCrateView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/user_create.html"
    success_url = reverse_lazy("login")

@login_required
def createPurchaseView(request,code):
    #per prelevare un solo oggetto e non un query set

    if request.method == "POST":

        p = Purchase()
        #ricerca diceset
        dice = Dice.objects.get(code__iexact= request.POST['setcode'])
        p.dice_set = dice
        #ricerca buyer
        buyer = User.objects.get(username__iexact=request.POST['buyer'])
        p.buyer = buyer
        p.date = datetime.datetime.now()
        p.amount_of_sets = request.POST['quantity']
        
        p.save()
        template= "store/sold.html"
        #per ora, non mi serve nulla
        ctx = {
            'spesa' : (float(dice.price)*float(p.amount_of_sets)),
        }
    else:
        dice = Dice.objects.get(code__iexact=code)
        template="store/purchase.html"
        ctx = {'dice' : dice,
            }
        
    ctx['MEDIA_URL'] = settings.MEDIA_URL
    
    return render(request, template_name=template, context=ctx)