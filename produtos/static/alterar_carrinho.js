let selects = document.getElementsByTagName('select')

for (let i = 0; i < selects.length; i++) {
  let select = selects[i];
  select.addEventListener('change', function() {
    let id_produto = select.id;
    let quantidade_produto = select.value;
    location.href = 'alterar/' + id_produto + '/' + quantidade_produto;
  })
}