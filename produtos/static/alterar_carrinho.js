function alterarCarrinho(id_produto) {
  var select_produto = document.getElementById('quantidade-' + id_produto);
  var quantidade_produto = select_produto.value;

  location.href = '/alterar_carrinho/' + id_produto + '/' + quantidade_produto
}