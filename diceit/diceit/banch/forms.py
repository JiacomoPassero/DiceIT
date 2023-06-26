from django import forms

from store.models import Dice
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CreateDiceForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addset_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit","Create Set"))


    class Meta:
        model = Dice
        fields = ["code",
                  "name",
                  "number_of_pices",
                  "number_of_pices",
                  'primary_color',
                  'description',
                  'seller',
                  'available',
                  'price',
                  'image'
                ]
    
    
    

