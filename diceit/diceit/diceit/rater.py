#inserisci il raccomandation sistem
from surprise import Dataset, Reader, KNNWithMeans
from django.contrib.auth.models import User
from store.models import Dice,Purchase
#per aggiornamento automatico del file del rating
import threading
import time
from . import settings

def set_up_prediction():
    reader = Reader(rating_scale=(1,10))

    data = Dataset.load_from_file('diceit/ratings.txt',reader)

    sim_options = {
        "name" : "cosine",
        "user_based" : True,
    }

    algo = KNNWithMeans(sim_options=sim_options)

    trainingSet = data.build_full_trainset()

    algo.fit(trainingSet)

    return algo

def set_up_reccomendation_file():
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

    f.close()


def update_file_automatico():
    while True:
        tim_sec=settings.ORE_AGGIORNAMENTO_RECSYS*60*60
        time.sleep(tim_sec)

        set_up_reccomendation_file()

# Create and start the thread
def start_update_thread():
    thread = threading.Thread(target=update_file_automatico)
    thread.start()
