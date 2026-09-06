import { API_TIPO_CULTURAL_URL, mostrarMensagem, apiFetch } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await listarTiposCulturais();
});

export async function listarTiposCulturais() {
    const lista = document.getElementById('lista-tipo-cultural');
    lista.innerHTML = '';

    let resposta = await apiFetch(API_TIPO_CULTURAL_URL);

    let dados = await resposta.json();

    if (dados.length == 0) {

        let div = document.createElement('div');
        div.className = 'text-center py-5';

        let divIcone = document.createElement('div');
        divIcone.className = 'mb-3';

        let icone = document.createElement('i');
        icone.className = 'bi bi-palette';
        icone.style.fontSize = '50px';
        icone.style.color = '#6c757d';

        divIcone.appendChild(icone);

        let h4 = document.createElement('h4');
        h4.className = 'mb-2';
        h4.textContent = 'Nenhum tipo_cultural cadastrado';

        let p = document.createElement('p');
        p.className = 'text-muted';
        p.textContent = 'Comece criando um tipo_cultural para classificar os pontos culturais.';

        let button = document.createElement('a');
        button.href = '#';
        button.className = 'btn btn-primary mt-3';
        button.textContent = 'Criar primeiro tipo_cultural';

        div.appendChild(divIcone);
        div.appendChild(h4);
        div.appendChild(p);
        div.appendChild(button);

        lista.appendChild(div);

        return;
    }

    dados.forEach(tipo_cultural => {

        let div = document.createElement('div');
        div.className = 'd-flex justify-content-between align-items-center border-bottom py-3';

        let informacoes = document.createElement('div');

        let nome = document.createElement('strong');
        nome.textContent = tipo_cultural.nome;

        informacoes.appendChild(nome);

        let botoes = document.createElement('div');
        botoes.className = 'd-flex gap-2';

        let editar = document.createElement('a');
        editar.href = `/admin/atualizar-tipo-cultural/${tipo_cultural.id}`;
        editar.className = 'btn btn-warning btn-sm';
        editar.title = 'Editar';

        let iconeEditar = document.createElement('i');
        iconeEditar.className = 'bi bi-pencil';

        editar.appendChild(iconeEditar);

        let excluir = document.createElement('button');
        excluir.type = 'button';
        excluir.className = 'btn btn-danger btn-sm d-flex align-items-center justify-content-center';
        excluir.title = 'Excluir';

        removertipo_cultural(excluir, tipo_cultural, div);

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

async function removertipo_cultural(botao, tipo_cultural, div) {
    botao.addEventListener('click', async () => {

        let confirmar = confirm(`Tem certeza que deseja excluir o tipo_cultural ${tipo_cultural.nome}?`);

        if (!confirmar) {
            return;
        }

        let respostaExcluir = await apiFetch(
            `${API_TIPO_CULTURAL_URL}/${tipo_cultural.id}`,
            {
                method: 'DELETE'
            }
        );

        let dadosExcluir = await respostaExcluir.json();

        div.remove();

        mostrarMensagem(dadosExcluir.mensagem, dadosExcluir.classe);
    });
}