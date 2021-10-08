from django import template

register = template.Library()


@register.filter(name='getvalues')
def getvalues(dicionario, categoria):
    return dicionario.get(categoria)


@register.filter(name='firstvalues')
def firstvalues(dicionario, categoria):
    return dicionario.get(categoria)[0]
