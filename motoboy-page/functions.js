function buscarPedidos(motoboyId) {
  fetch(`https://projeto-integrador-2-0rhf.onrender.com/pedido/motoboy/${motoboyId}`)
    .then((response) => response.json())
    .then((data) => {
      exibirMotoboy(data.motoboy);
      exibirPedidos(data.pedidos);
      console.log(data);
    })
    .catch((error) => console.error("Erro ao buscar pedidos:", error));
}

function exibirMotoboy(motoboy) {
  document.getElementById("motoboy").innerText = motoboy.nome;
}

function exibirPedidos(pedidos) {
  const listaPedidos = document.getElementById("lista-pedidos");
  listaPedidos.innerHTML = "";

  let pedidosEntregues = 0;

  // Obter a data atual no timezone de São Paulo
  const dataAtual = new Date().toLocaleDateString("pt-BR", {
    timeZone: "America/Sao_Paulo",
  });

  // Filtrar pedidos para incluir apenas os pedidos do dia atual
  const pedidosDoDia = pedidos.filter((pedido) => {
    console.log(pedido)
    if (!pedido.data_hora_inicio) return false;

    try {
      const dataPedido = new Date(pedido.data_hora_inicio).toLocaleDateString(
        "pt-BR",
        { timeZone: "America/Sao_Paulo" }
      );
      console.log(dataPedido)
      return dataPedido === dataAtual;
    } catch (error) {
      console.error("Erro ao converter data:", pedido.data_hora_inicio, error);
      return false;
    }
  });

  console.log(pedidosDoDia);

  // Exibir os pedidos filtrados
  pedidosDoDia.forEach((pedido) => {
    const pedidoDiv = document.createElement("div");
    pedidoDiv.classList.add("pedido-info");

    pedidoDiv.innerHTML = `
      <p style="color: green;"><strong>Pedido:</strong> ${pedido.id}</p>
      <div class="pedidoDivWrapper">
        <ul>
          ${pedido.produtos.map((produto) => `<li>${produto.nome}</li>`).join("")}
        </ul>
      </div>
      <p><strong>Total:</strong> R$${pedido.total_pedido.toFixed(2)}</p>
      <p id="status-entrega"><strong>Status:</strong> ${pedido.status}</p>
    `;

    const clienteInfo = pedido.cliente
      ? `
          <p><strong>Cliente:</strong> ${pedido.cliente.nome}<br>
             <strong>Endereço:</strong> ${pedido.cliente.logradouro}, ${pedido.cliente.numero}${pedido.cliente.complemento ? `, ${pedido.cliente.complemento}` : ''}<br>
             <strong>Bairro:</strong> ${pedido.cliente.bairro}<br>
             <strong>Telefone:</strong> ${pedido.cliente.telefone}</p>
        `
      : `<p>Cliente não especificado</p>`;

    pedidoDiv.innerHTML += clienteInfo;

    if (pedido.status === "Em andamento") {
      const entregarCheckbox = criarCheckboxComLabel(
        `entregar-${pedido.id}`,
        "Entregar",
        listaPedidos,
        pedidoDiv
      );
      const cancelarCheckbox = criarCheckboxComLabel(
        `cancelar-${pedido.id}`,
        "Cancelar",
        listaPedidos,
        pedidoDiv
      );

      entregarCheckbox.addEventListener("click", () => {
        if (entregarCheckbox.checked) {
          confirmarOuCancelarEntrega(pedido.id, "entregar", listaPedidos);
        }
      });

      cancelarCheckbox.addEventListener("click", () => {
        if (cancelarCheckbox.checked) {
          confirmarOuCancelarEntrega(pedido.id, "cancelar", listaPedidos);
        }
      });
    }

    if (pedido.data_hora_finalizacao !== null) {
      const dataHoraFinalizacao = new Date(pedido.data_hora_finalizacao);
      const horaFinalizacao = dataHoraFinalizacao.toLocaleTimeString("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
        timeZone: "America/Sao_Paulo",
      });

      pedidoDiv.innerHTML += `<p><strong>Hora de Finalização:</strong> ${horaFinalizacao}</p>`;
    }

    listaPedidos.appendChild(pedidoDiv);

    if (pedido.status === "Entregue") {
      pedidosEntregues++;
    }
  });

  // Atualizar o contador de entregas e o valor a receber
  document.getElementById("entregas-feitas").textContent = pedidosEntregues;
  var valor = pedidosEntregues * 5;
  document.getElementById("valor-a-receber").innerHTML = valor.toLocaleString(
    "pt-BR",
    { style: "currency", currency: "BRL" }
  );
}


function criarCheckboxComLabel(id, labelText, listaPedidos, parentElement) {
  const checkboxLabel = document.createElement("label");
  checkboxLabel.htmlFor = id;
  checkboxLabel.innerText = labelText;

  const checkbox = document.createElement("input");
  checkbox.type = "checkbox";
  checkbox.id = id;

  parentElement.appendChild(checkboxLabel);
  parentElement.appendChild(checkbox);

  return checkbox;
}

function confirmarOuCancelarEntrega(idPedido, acao, listaPedidos) {
  const endpoint = ` https://projeto-integrador-2-0rhf.onrender.com/pedido/${idPedido}/action/${acao}`;
  console.log(`Chamando endpoint: ${endpoint}`);

  const requestOptions = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  };

  fetch(endpoint, requestOptions)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erro ao chamar o endpoint.");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Requisição bem-sucedida:", data);
      console.log("Recarregando a página...");
      window.location.reload();
    })
    .catch((error) => {
      console.error("Erro:", error);
      console.log("Ocorreu um erro ao processar o pedido.");
    });
}

window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const motoboyId = urlParams.get("motoboy");

  if (motoboyId) {
    buscarPedidos(motoboyId);
  } else {
    console.error('Parâmetro "motoboy" não encontrado na URL.');
  }
};
