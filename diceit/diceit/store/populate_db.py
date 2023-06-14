from store.models import User, Dice, Purchase

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

    for i in range(0,10):
        u = User()
        u.username = utenti[i]
        u.password = password[i]
        u.mail = mail[i]

        u.save()

    print(User.objects.all())

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
        "G",
        "B",
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

    for i in range(0,10):
        d = Dice()
        d.code = code[i]
        d.name = names[i]
        d.number_of_pices = number_of_pices[i]
        d.primary_color = primary_colors[i]
        d.description = descriptions[i]
        d.seller = None
        d.available = False
        d.price = prices[i]
        d.save()
    
    print(Dice.objects.all())



def erase_db():
    User.objects.all().delete()
    Dice.objects.all().delete()
    Purchase.objects.all().delete()
        
