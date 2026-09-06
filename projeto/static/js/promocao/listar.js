import { API_PROMOCAO_URL, mostrarMensagem, apiFetch } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await listarPromocoes();
});

function formatarData(data) {
    let [ano, mes, dia] = data.split('-');
    return `${dia}/${mes}/${ano}`;
}

export async function listarPromocoes() {
    const lista = document.getElementById('lista-promocoes');
    lista.innerHTML = '';

    let resposta = await apiFetch(API_PROMOCAO_URL);

    let dados = await resposta.json();

    if (dados.length == 0) {

        let div = document.createElement('div');
        div.className = 'text-center py-5';

        let divIcone = document.createElement('div');
        divIcone.className = 'mb-3';

        let icone = document.createElement('i');
        icone.className = 'bi bi-tags';
        icone.style.fontSize = '50px';
        icone.style.color = '#6c757d';

        divIcone.appendChild(icone);

        let h4 = document.createElement('h4');
        h4.className = 'mb-2';
        h4.textContent = 'Nenhuma promoção cadastrada';

        let p = document.createElement('p');
        p.className = 'text-muted';
        p.textContent = 'Comece cadastrando uma promoção para aplicar aos pontos turísticos.';

        let button = document.createElement('a');
        button.href = '#';
        button.className = 'btn btn-primary mt-3';
        button.textContent = 'Cadastrar primeira promoção';

        div.appendChild(divIcone);
        div.appendChild(h4);
        div.appendChild(p);
        div.appendChild(button);

        lista.appendChild(div);

        return;
    }

    dados.forEach(promocao => {

        let div = document.createElement('div');
        div.className = 'd-flex justify-content-between align-items-center border-bottom py-3';

        let informacoes = document.createElement('div');

        let titulo = document.createElement('strong');
        titulo.textContent = promocao.titulo;

        informacoes.appendChild(titulo);
        informacoes.appendChild(document.createElement('br'));

        if (promocao.descricao) {
            let descricao = document.createElement('small');
            descricao.className = 'text-muted';
            descricao.textContent = promocao.descricao;

            informacoes.appendChild(descricao);
            informacoes.appendChild(document.createElement('br'));
        }

        let desconto = document.createElement('small');
        desconto.className = 'text-muted';
        desconto.textContent = `${promocao.desconto}% de desconto`;

        informacoes.appendChild(desconto);
        informacoes.appendChild(document.createElement('br'));

        let datas = document.createElement('small');
        datas.className = 'text-muted';
        datas.textContent = `${formatarData(promocao.data_inicio)} até ${formatarData(promocao.data_fim)}`;

        informacoes.appendChild(datas);

        let botoes = document.createElement('div');
        botoes.className = 'd-flex gap-2';

        let editar = document.createElement('a');
        editar.href = `/admin/editar-promocao/${promocao.id}`;
        editar.className = 'btn btn-warning btn-sm';
        editar.title = 'Editar';

        let iconeEditar = document.createElement('i');
        iconeEditar.className = 'bi bi-pencil';

        editar.appendChild(iconeEditar);

        let excluir = document.createElement('button');
        excluir.type = 'button';
        excluir.className = 'btn btn-danger btn-sm d-flex align-items-center justify-content-center';
        excluir.title = 'Excluir';

        removerPromocao(excluir, promocao, div);

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

async function removerPromocao(botao, promocao, div) {
    botao.addEventListener('click', async () => {

        let confirmar = confirm(`Tem certeza que deseja excluir a promoção ${promocao.titulo}?`);

        if (!confirmar) {
            return;
        }

        let respostaExcluir = await apiFetch(
            `${API_PROMOCAO_URL}/${promocao.id}`,
            {
                method: 'DELETE'
            }
        );

        let dadosExcluir = await respostaExcluir.json();

        div.remove();

        mostrarMensagem(dadosExcluir.mensagem, dadosExcluir.classe);
    });
}