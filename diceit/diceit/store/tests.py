from django.test import TestCase
from diceit import rater
import datetime
from django.urls import reverse
#Create your tests here

'''il raccomendation system interagisce con il database e i suoi modelli, e sembra che utilizzare i model temporanei durante la fase
di test disturbi il suo comportamento, di conseguenza è necessario rimuovere l'inizializzazione del predittore nel file
diceit/urls.py e di seguidi riprodurre il funzionamento del tester con dati già prodotti in precedenza.
E' un funzionamento poco fluido ma essendo la funzionalità più importante del progetto preferisco utilizzarla come test replicando
il codice piùttosto che utilizzare un altra parte del sistema meno prioritaria'''

class TestRaccomendation(TestCase):

    pred = rater.set_up_prediction()
    
    def test_dati_coerenti(self):

        

        previsione = self.pred.predict('xX_Capodieci_Xx','D8')

        #la previsione deve essere nel range accettabile
        self.assertGreaterEqual(previsione.est,0.0)
        self.assertLessEqual(previsione.est,10.0)

    def test_dati_non_coerenti_user(self):

        
        
        previsione = self.pred.predict('non_esistente','D8')
        
        #4 indice dizionario informazioni
        possibile = previsione[4]['was_impossible']
        
        #la previsione deve riconoscere un errore
        self.assertEqual(possibile,True)
        #tuttavia deve anche restituire un valore per garantire il funzionamento del programma
        self.assertGreaterEqual(previsione.est,0.0)
        self.assertLessEqual(previsione.est,10.0)

    def test_dati_non_coerenti_set(self):

        
        
        previsione = self.pred.predict('xX_Capodieci_Xx','XXX')
        
        #4 indice dizionario informazioni
        possibile = previsione[4]['was_impossible']
        
        #la previsione deve riconoscere un errore
        self.assertEqual(possibile,True)
        #tuttavia deve anche restituire un valore per garantire il funzionamento del programma
        self.assertGreaterEqual(previsione.est,0.0)
        self.assertLessEqual(previsione.est,10.0)

    def test_dati_insensati(self):

        parametri_1 = [23,"Ginevra",datetime.datetime.now(),None,r"quelquechose"]
        parametri_2 = [{"un dizionario":2,"bello":89},13,None,type(True),'C']
        
        for i in range(1,5):

            previsione = self.pred.predict(parametri_1[i],parametri_2[i])
            
            #4 indice dizionario informazioni
            possibile = previsione[4]['was_impossible']
            
            #la previsione deve riconoscere un errore
            self.assertEqual(possibile,True)
            #tuttavia deve anche restituire un valore per garantire il funzionamento del programma
            self.assertGreaterEqual(previsione.est,0.0)
            self.assertLessEqual(previsione.est,10.0)

    def test_permessi_view(self):
        #accesso ad aree riservate, devo essere bloccato e redirezionat
        response = self.client.get(reverse('banch:banch'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('hoard:hoard'))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('diventa_artigiano'))
        self.assertEqual(response.status_code, 302)
        
        

