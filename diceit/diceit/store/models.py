from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

'''
class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=150)
    mail = models.CharField(max_length=100)

    def __str__(self):
        out = self.username
        if self.mail == None:
            out += " : no mail associated"
        else:
            out += " : "+self.mail
    
        return out
'''

class Dice(models.Model):
    COLORS = [
        ("R","Red"),
        ("O","Orange"),
        ("Y","Yellow"),
        ("G","Green"),
        ("B","Blue"),
        ("P","Purple"),
        ("N","Black"),
        ("W","White"),
        ("M","Metal"),
    ]
    
    code = models.CharField(max_length=255, primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    number_of_pices = models.PositiveSmallIntegerField()
    primary_color = models.CharField(max_length=1, choices=COLORS)
    description = models.CharField(max_length=300)
    #seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    available = models.BooleanField()
    price = models.FloatField()
    #zona immagine
    image = models.ImageField(upload_to='uploads/',null= True)
    #uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        out = self.name + " of " + str(self.number_of_pices) + " pieces"
        if self.seller == None:
            out += " not available"
        else:
            out += " sold by " + self.seller.username
        return out
    
 
class Purchase(models.Model):
    dice_set = models.ForeignKey(Dice, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount_of_sets = models.PositiveIntegerField()

    def __str__(self):
        out = "Set "+ str(self.dice_set) + " bought by "+ self.buyer.username + " on date " + str(self.date)
        return out
