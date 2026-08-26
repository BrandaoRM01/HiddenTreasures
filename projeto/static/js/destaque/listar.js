import { API_DESTAQUE_URL, mostrarMensagem } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await listarDestaques();
});

export async function listarDestaques() {
    const lista = document.getElementById('lista-destaques');
    lista.innerHTML = '';

    let resposta = await fetch(API_DESTAQUE_URL);

    let dados = await resposta.json();

    if (dados.length == 0) {

        let div = document.createElement('div');
        div.className = 'text-center py-5';

        let divIcone = document.createElement('div');
        divIcone.className = 'mb-3';

        let icone = document.createElement('i');
        icone.className = 'bi bi-star-fill';
        icone.style.fontSize = '50px';
        icone.style.color = '#6c757d';

        divIcone.appendChild(icone);

        let h4 = document.createElement('h4');
        h4.className = 'mb-2';
        h4.textContent = 'Nenhum destaque cadastrado';

        let p = document.createElement('p');
        p.className = 'text-muted';
        p.textContent = 'Comece criando um destaque para os pontos turísticos.';

        let button = document.createElement('a');
        button.href = '#';
        button.className = 'btn btn-primary mt-3';
        button.textContent = 'Criar primeiro destaque';

        div.appendChild(divIcone);
        div.appendChild(h4);
        div.appendChild(p);
        div.appendChild(button);

        lista.appendChild(div);

        return;
    }

    dados.forEach(destaque => {

        let div = document.createElement('div');
        div.className = 'd-flex justify-content-between align-items-center border-bottom py-3';

        let informacoes = document.createElement('div');

        let nome = document.createElement('strong');
        nome.textContent = destaque.nome;

        informacoes.appendChild(nome);

        let botoes = document.createElement('div');
        botoes.className = 'd-flex gap-2';

        let editar = document.createElement('a');
        editar.href = `/admin/atualizar-destaque/${destaque.id}`;
        editar.className = 'btn btn-warning btn-sm';
        editar.title = 'Editar';

        let iconeEditar = document.createElement('i');
        iconeEditar.className = 'bi bi-pencil';

        editar.appendChild(iconeEditar);

        let excluir = document.createElement('button');
        excluir.type = 'button';
        excluir.className = 'btn btn-danger btn-sm d-flex align-items-center justify-content-center';
        excluir.title = 'Excluir';

        removerDestaque(excluir, destaque, div);

        let iconeExcluir = document.createElement('i');
        iconeExcluir.className = 'bi bi-trash';

        excluir.appendChild(iconeExcluir);

        botoes.appendChild(editar);
        botoes.appendChild(excluir);

        div.appendChild(informacoes);
        div.appendChild(botoes);

        lista.appendChild(div);
    });
}

async function removerDestaque(botao, destaque, div) {
    botao.addEventListener('click', async () => {

        let confirmar = confirm(`Tem certeza que deseja excluir o destaque ${destaque.nome}?`);

        if (!confirmar) {
            return;
        }

        let respostaExcluir = await fetch(
            `${API_DESTAQUE_URL}/${destaque.id}`,
            {
                method: 'DELETE'
            }
        );

        let dadosExcluir = await respostaExcluir.json();

        div.remove();

        mostrarMensagem(dadosExcluir.mensagem, dadosExcluir.classe);
    });
}