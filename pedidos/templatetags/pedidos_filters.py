from django import template

register = template.Library()

@register.filter(name='get_image')
def get_image(dicionario, chave):
    return dicionario.get(chave).produto.imagem.path


@register.filter(name='multi')
def multiplication(num1, num2):
    return num1 * num2
