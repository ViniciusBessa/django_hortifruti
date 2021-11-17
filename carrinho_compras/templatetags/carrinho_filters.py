from django import template

register = template.Library()


@register.filter(name='get_quantidade')
def get_quantidade(produto, dicionario):
    return dicionario.get(produto)

@register.filter(name='range_estoque')
def range_estoque(estoque):
    if estoque >= 5:
        return range(1, 6)
    return range(1, estoque + 1)
