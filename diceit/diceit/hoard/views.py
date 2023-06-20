from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random

# Create your views here.
@login_required
def hoard(request):
    dice_faces = ('⚀',
                  "⚁",
                  "⚂",
                  "⚃",
                  "⚄",
                  "⚅",
                  )
    
    card1 ={'title': 'Your Hoard',
            'subtitle' : 'Check your purchases',
            'dice' : random.choice(dice_faces),
        }
    card2 ={'title': 'Other Hoards',
            'subtitle' : "Take inspiration from other people' collection",
            'dice' : random.choice(dice_faces),
        }
    cards=(card1,card2)
    ctx = {
        'cards' : cards,
        'lucky' : (card1['dice'] == card2['dice']),
    }
    
    return render(request, template_name='hoard/hoard.html', context=ctx)