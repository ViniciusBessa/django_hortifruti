// Função que modifica a cor de fundo do main se a página for um formulário
function VerificarFormulario() {
  let formulario = document.getElementById('formulario');
  if (formulario) {
    let main = document.getElementById('main');
    main.className = "cor-secundaria tamanho-pagina mt-5 pt-4";
  }
}

VerificarFormulario()