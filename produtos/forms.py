from django import forms
from .models import Transportadora, FormaPagamento


class FinalizarPedido(forms.Form):
    """
    Formulário para receber qual opção de transportadora e forma de pagamento o usuário deseja

    Attribute transportadora: Recebe a opção de transportadora que o usuário escolher
    Attribute forma_pagamento: Recebe a opção de forma de pagamento que o usuário escolher
    """

    transportadora = forms.ChoiceField(choices=[], widget=forms.RadioSelect)
    forma_pagamento = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transportadora'].choices = Transportadora.receber()
        self.fields['forma_pagamento'].choices = FormaPagamento.receber()
