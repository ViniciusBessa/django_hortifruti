let selects = document.getElementsByTagName('select');

for (let i = 0; i < selects.length; i++) {
  let select = selects[i];
  select.addEventListener('change', function() {
    let idProduto = select.id;
    let quantidadeProduto = select.value;
    location.href = 'alterar/' + idProduto + '/' + quantidadeProduto;
  })
}