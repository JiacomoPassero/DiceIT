from store.models import Dice, Purchase
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import datetime

'''Attenzione: con questo metodo le password non sono salvate cifrate, quindi il login fallisce se creano gli utenti
con questa funzione'''
def create_users_db():
    #q = User.objects.all()

    utenti = (
        "xX_Capodieci_Xx",
        "TheDiceAddicted",
        "LikeADragon",
        "Mario",
        "Lidia078",
        "whatimdoingwithmyLife",
        "UnCanalePerIlFuturo",
        "Yoshi",
        "ToruBestWaifu",
        "GinoPippo"
    )
    #Saranno belli da ricordare
    password = (
        "C4p0d13c1!",
        "Add1ct3d!",
        "L1k3_Dr4g0n!",
        "Sup3r_Fr4t3ll0!",
        "C4rr0_Arm4t0!",
        "N3ckR0p3Swing",
        "Prg0gr3ss0!",
        "S4cr1f1c10!",
        "M41dDr4g0n!",
        "S4nFr4nc3sc0!"
    )

    '''
    mail = (
        "capo.10@gmail.com",
        "dice@gmail.com",
        "drago@gmail.com",
        "mario@gmail.com",
        "lidia078@gmail.com",
        "life@gmail.com",
        "canali@gmail.com",
        "yoshi@gmail.com",
        "toru@gmail.com",
        "gino.pippo@gmail.com"
    )
    '''

    for i in range(0,10):
        u = User()
        u.username = utenti[i]
        u.password = password[i]
        
        u.save()

    print(User.objects.all())
'''Attenzione: questa è una funzione deprecata poichè i dadi vengono creati senza associare dei file immagice ad essi'''
def create_dices_db():
    code = (
        "D1",
        "D2",
        "D3",
        "D4",
        "D5",
        "D6",
        "D7",
        "D8",
        "D9",
        "D10"
    )

    names = (
        "Dadi rossi",
        "Dadi arancioni",
        "Dadi gialli",
        "Dadi Verdi",
        "Dadi Blue",
        "Dadi Viola",
        "Dadi Arcobaleno",
        "Dadi Metallo",
        "Dadi Cosmo",
        "Dadi Bullet"
    )

    number_of_pices = (
        7,
        7,
        7,
        7,
        7,
        7,
        7,
        7,
        7,
        6
    )

    primary_colors = (
        "R",
        "O",
        "Y",
        "G",
        "B",
        "P",
        "W",
        "M",
        "N",
        "Y"
    )

    descriptions = (
        "Dadi dal colore rosso",
        "Dadi dal colore Arancione",
        "Dadi dal colore Giallo",
        "Dadi dal colore Verde",
        "Dadi dal colore Blu",
        "Dadi dal colore Viola",
        "Dadi semitrasparenti il cui colore cambia in base a come la luce li colpisce",
        "Dadi metallici con incisioni sulla superficie",
        "Dadi neri, semitrasparenti con decorazioni che richiamando alle immagini dello spazio profondo",
        "Set di dadi a sei facce a forma di proiettile"
    )

    #seller

    prices = (
        7.99,
        7.99,
        7.99,
        7.99,
        7.99,
        7.99,
        18.5,
        12.45,
        15.5,
        13.14        
    )

     #i due artigiani
    u1 = User.objects.get(username__iexact="GinoPippo")
    u2 = User.objects.get(username__iexact="Yoshi")

    for i in range(0,10):
        d = Dice()
        d.code = code[i]
        d.name = names[i]
        d.number_of_pices = number_of_pices[i]
        d.primary_color = primary_colors[i]
        d.description = descriptions[i]
        if(i % 2):
            d.seller = u1
        else:
            d.seller = u2
        d.available = True
        d.price = prices[i]
        #a quanto pare non riesco a passare un singolo file usando python
        d.image = "../static/set/set_"+str(d.code)+".png"
        d.save()
    
    print(Dice.objects.all())

'''Funzione di creazione di acquisti, da lanciare dopo aver creato gli utenti e i dadi'''
def create_purchases_db():
    #creazione prima orda
    u = User.objects.get(username__iexact="xX_Capodieci_Xx")
    d = Dice.objects.get(code__iexact='D9')
    datetime_object = datetime.datetime(2023,6,20)

    p = Purchase()
    p.dice_set = d
    p.buyer = u
    p.date = datetime_object
    p.amount_of_sets = 7
    p.save()

    #creazione seconda orda

    u = User.objects.get(username__iexact="TheDiceAddicted")
    datetime_object = datetime.datetime(2023,6,29)

    for i in ('D1','D2','D3','D4','D5','D6','D7','D8','D9','D10'):
        p = Purchase()
        d = Dice.objects.get(code__iexact=i)
        p.dice_set = d
        p.buyer = u
        p.date = datetime_object
        p.amount_of_sets = 10
        p.save()
    
    #creazione terza orda
    u = User.objects.get(username__iexact="LikeADragon")
    datetime_object = datetime.datetime(2023,6,24)

    for i in ('D1','D3','D5','D6','D7','D9','D10'):
        p = Purchase()
        d = Dice.objects.get(code__iexact=i)
        p.dice_set = d
        p.buyer = u
        p.date = datetime_object
        p.amount_of_sets = 8
        p.save()

'''Funzione che rimove i dadi e gli acquisti''' 
def erase_db():
    #User.objects.exclude(username="admin").delete()
    Dice.objects.all().delete()
    Purchase.objects.all().delete()
'''Funzione che rimuove solo gli acquisti'''
def erase_purchase():
    Purchase.objects.all().delete()

'''Funzione per popolare le prime versioni del database, soffre delle mancanze delle altre funzione che usa.
Deprecata'''
def populate_db():
    #create_users_db()
    create_dices_db()
    create_purchases_db()
    #creazione gruppi utenti
    Group.objects.get_or_create(name='artigiani')
    artigiani = Group.objects.get(name='artigiani')
    u = User.objects.get(username__iexact="GinoPippo")
    artigiani.user_set.add(u)
    u = User.objects.get(username__iexact="Yoshi")
    artigiani.user_set.add(u)
    #definizone permessi