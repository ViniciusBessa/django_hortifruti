var motor_busca = document.getElementById('motor-busca')
var action_busca = motor_busca.action

function Busca() {
  let busca_do_usuario = document.getElementById('busca-usuario')
  motor_busca.action = '/busca/' + busca_do_usuario.value
}
