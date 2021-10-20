from django import template

register = template.Library()


@register.filter(name='get_values')
def get_values(dicionario, categoria):
    return dicionario.get(categoria)


@register.filter(name='first_value')
def first_value(dicionario, categoria):
    return dicionario.get(categoria)[0]


@register.filter(name='get_quantidade')
def get_quantidade(produto, dicionario):
    return dicionario.get(produto)


@register.filter(name='range')
def range(comeco, fim):
    lista = []
    for num in range(comeco, fim + 1):
        lista.append(num)
    print(lista)
    return lista
