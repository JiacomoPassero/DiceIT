from django.shortcuts import render
from store.models import User, Dice

# Create your views here.
def store(request):

    dices = Dice.objects.all()

    ctx = { 
            'dices' :   dices,
        }

    return render(request, template_name='store/store.html', context=ctx)