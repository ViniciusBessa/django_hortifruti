let motorBusca = document.getElementById('motor-busca')
let botaoBusca = document.getElementById('botao-busca')

botaoBusca.addEventListener('click', function() {
  let buscaDoUsuario = document.getElementById('busca-usuario')
  motorBusca.action = '/busca/' + buscaDoUsuario.value
})