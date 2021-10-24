function alterarCarrinho(id_produto) {
  let select_produto = document.getElementById('quantidade-' + id_produto);
  let quantidade_produto = select_produto.value;

  location.href = '/alterar_carrinho/' + id_produto + '/' + quantidade_produto
}