let selects = document.getElementsByTagName("select");
selects = Array.from(selects);

selects.forEach(function (item) {
  item.addEventListener("change", function () {
    let idProduto = item.id;
    let quantidadeProduto = item.value;
    location.href = "alterar/" + idProduto + "/" + quantidadeProduto;
  });
});
