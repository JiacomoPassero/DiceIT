from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import random
from braces.views import GroupRequiredMixin
from store.models import Dice



from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CreateDiceForm



# Create your views here.
def has_group(user):
    return user.groups.filter(name="artigiani").exists()

@user_passes_test(has_group)
def banch(request):
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
    return render(request, template_name='banch/banch.html', context=ctx)


class CreateDiceView(GroupRequiredMixin, CreateView):
    group_required = ['artigiani']
    title = 'Create a new set'
    form_class = CreateDiceForm
    model = Dice
    template_name = 'banch/create_set.html'
    success_url = reverse_lazy("banch:modify_set")        
    
def modify_set(request):
    d = Dice.objects.all()
    ctx = {'dices' : d}
    return render(request, template_name='banch/modify_set.html', context=ctx)