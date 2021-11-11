from django import forms
from .models import Transportadora, FormaPagamento


class FinalizarPedido(forms.Form):
    transportadora = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
    forma_pagamento = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
  

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['transportadora'].choices = Transportadora.receber()
        self.fields['forma_pagamento'].choices = FormaPagamento.receber()
