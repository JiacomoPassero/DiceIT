#inserisci il raccomandation sistem
from surprise import Dataset, Reader, KNNWithMeans
from django.contrib.auth.models import User
from store.models import Dice,Purchase
#per aggiornamento automatico del file del rating
import threading
import time
from . import settings

'''Funzione di lettura del file dei ratings che iniziarisma l'oggetto per eseguire le predizioni.'''
def set_up_prediction(file=None):
    if file == None:
        file = 'diceit/ratings.txt'
    reader = Reader(rating_scale=(1,10))

    data = Dataset.load_from_file(file,reader)

    sim_options = {
        "name" : "cosine",
        "user_based" : True,
    }

    algo = KNNWithMeans(sim_options=sim_options)

    trainingSet = data.build_full_trainset()

    algo.fit(trainingSet)

    return algo

'''Algoritmo che a partire dal model crea il file che verrà utilizzato per fare il setup dell'algoritmo.
Inizializza un valore e un rating per ogni utente-acquisto, dando il punteggio minimo nel caso la coppia non esiste.
il rating dipende dal numero di volte che un utente ha comprato un set di dadi, in scala 1-10.
Viene richiamato all'avvio del sito e ad intervalli di tempo regolari successivamente'''
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

'''Funzione che aggiorna automaticamente il file dei rating, il numero di ore di attesa per ripetere il processo e specificato
in settings.py'''
def update_file_automatico():
    while True:
        tim_sec=settings.ORE_AGGIORNAMENTO_RECSYS*60*60
        time.sleep(tim_sec)

        set_up_reccomendation_file()

'''Funzione di avvio del thread di aggiornamento del file'''
def start_update_thread():
    thread = threading.Thread(target=update_file_automatico)
    thread.start()
