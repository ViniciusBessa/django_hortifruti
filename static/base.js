function buscar() {
  let form = document.getElementById('formBusca')
  let input = document.getElementById('inputBusca')

  form.action = '/busca/' + input.value
}
