from django import template

register = template.Library()


@register.filter(name='getvalues')
def getvalues(dicionario, categoria):
    return dicionario[categoria]


@register.filter(name='firstvalues')
def firstvalues(dicionario, categoria):
    return dicionario[categoria][0]
