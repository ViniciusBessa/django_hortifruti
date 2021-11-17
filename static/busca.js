let motor_busca = document.getElementById('motor-busca')
let action_busca = motor_busca.action
let botao_busca = document.getElementById('botao-busca')

botao_busca.addEventListener('click', function() {
  let busca_do_usuario = document.getElementById('busca-usuario')
  motor_busca.action = '/busca/' + busca_do_usuario.value
})