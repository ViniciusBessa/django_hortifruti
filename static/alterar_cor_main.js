// Função que modifica a cor de fundo do main se a página for um formulário
function VerificarFormulario() {
  formulario = document.getElementById('formulario');
  console.log(formulario)
  if (formulario) {
      main = document.getElementById('main');
      main.className = "cor-primaria tamanho-pagina mt-5 pt-4";
  }
}

VerificarFormulario()