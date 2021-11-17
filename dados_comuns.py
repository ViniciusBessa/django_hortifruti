from produtos.models import CategoriasProduto
from carrinho_compras.models import CarrinhoCompra

def dados_comuns(usuario):
    """Função que retorna o número de produtos no carrinho e todas categorias registradas, 
       dados que são utilizados em diversas partes do projeto"""

    carrinho_compra = CarrinhoCompra.receber(usuario)
    categorias = list(CategoriasProduto.objects.all())
    return {
        'categorias': categorias,
        'numero_produtos_carrinho': len(carrinho_compra),
    }
