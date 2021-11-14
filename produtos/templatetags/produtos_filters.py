from django import template

register = template.Library()


@register.filter(name='get_values')
def get_values(dicionario, chave):
    return dicionario.get(chave)


@register.filter(name='get_quantidade')
def get_quantidade(produto, dicionario):
    return dicionario.get(produto)


@register.filter(name='get_image')
def get_image(dicionario, chave):
    return dicionario.get(chave).id_produto.imagem.path


@register.filter(name='range_estoque')
def range_estoque(estoque):
    if estoque >= 5:
        return range(1, 6)
    return range(1, estoque + 1)

@register.filter(name='multi')
def multiplication(num1, num2):
    return num1 * num2
