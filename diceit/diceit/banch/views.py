from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import random
from braces.views import GroupRequiredMixin
from store.models import Dice

from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .forms import CreateDiceForm
from django.contrib.auth.models import User
from diceit import rater



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
        'artigiano' : True
    }
    return render(request, template_name='banch/banch.html', context=ctx)


class CreateDiceView(GroupRequiredMixin, CreateView):
    group_required = ['artigiani']
    title = 'Create a new set'
    form_class = CreateDiceForm
    model = Dice
    template_name = 'banch/create_set.html'
    success_url = reverse_lazy("banch:banch")  
 

@user_passes_test(has_group)
def view_sets(request):
    #essendo il redirect della create view, devo aggiornare il file dei rating per avere una valutazione coerente in store
    rater.set_up_reccomendation_file()
    #Posso accedere a questa pagina solo da loggato, quindi non controllo di non essere loggato
    username = request.user.username
    user = User.objects.get(username__iexact=username)
    d = Dice.objects.filter(seller__exact=user)
    ctx = {'dices' : d}
    ctx['artigiano'] = True
    return render(request, template_name='banch/view_sets.html', context=ctx)

class UpdateDiceView(GroupRequiredMixin,UpdateView):
    group_required = ['artigiani']
    model = Dice
    template_name = "banch/modify_set.html"
    fields = [
            "name",
            "number_of_pices",
            'primary_color',
            'description',
            'available',
            'price',
            ]
    
    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("store:purchase",kwargs={'code': pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artigiano'] = True
        return context




