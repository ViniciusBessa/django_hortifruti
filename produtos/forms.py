from django import forms
from django import forms
from .models import Transportadora, FormaPagamento


class FinalizarPedido(forms.Form):
    transportadoras = [[transportadora.id, transportadora.titulo] for transportadora in Transportadora.objects.all()]
    formas_pagamento = [[forma_pagamento.id, forma_pagamento.titulo] for forma_pagamento in FormaPagamento.objects.all()]
    transportadora = forms.ChoiceField(choices=transportadoras, widget=forms.RadioSelect, label='')
    forma_pagamento = forms.ChoiceField(choices=formas_pagamento, widget=forms.RadioSelect)
