from django import template

register = template.Library()


@register.filter(name='get_values')
def get_values(dicionario, chave):
    return dicionario.get(chave)
