import { API_PONTO_URL, mostrarMensagem, apiFetch, protegerRota } from '../main.js';

const API_SUGESTOES_URL = `${API_PONTO_URL}/sugestoes`;

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota(['admin', 'superadmin']);
    if (!usuario) return;

    await listarSugestoes();
});

export async function listarSugestoes() {
    let lista = document.getElementById('lista-sugestoes');
    lista.innerHTML = '';

    let resposta = await apiFetch(API_SUGESTOES_URL);
    let dados = await resposta.json();

    if (dados.length == 0) {
        let div = document.createElement('div');
        div.className = 'text-center py-5';

        let icone = document.createElement('i');
        icone.className = 'bi bi-check2-circle display-1 text-success';

        let h3 = document.createElement('h3');
        h3.className = 'mt-3';
        h3.textContent = 'Nenhuma sugestão pendente';

        let p = document.createElement('p');
        p.className = 'text-muted mb-0';
        p.textContent = 'Todas as sugestões já foram analisadas.';

        div.appendChild(icone);
        div.appendChild(h3);
        div.appendChild(p);

        lista.appendChild(div);

        return;
    }

    let linha = document.createElement('div');
    linha.className = 'row g-3';

    dados.forEach(ponto => {
        linha.appendChild(criarCartaoSugestao(ponto));
    });

    lista.appendChild(linha);
}

function criarCartaoSugestao(ponto) {
    let coluna = document.createElement('div');
    coluna.className = 'col-12';

    let cartao = document.createElement('div');
    cartao.className = 'card shadow-sm border-0';

    let corpoCartao = document.createElement('div');
    corpoCartao.className = 'card-body';

    let linhaInterna = document.createElement('div');
    linhaInterna.className = 'row align-items-center';

    let colunaInfo = document.createElement('div');
    colunaInfo.className = 'col-lg-8';

    let grupoImagem = document.createElement('div');
    grupoImagem.className = 'd-flex align-items-center gap-3';

    let imagem = document.createElement('img');
    imagem.src = `/static/${ponto.url_imagem}`;
    imagem.alt = ponto.nome;
    imagem.className = 'rounded shadow-sm';
    imagem.style.width = '100px';
    imagem.style.height = '100px';
    imagem.style.objectFit = 'cover';

    let textos = document.createElement('div');

    let nome = document.createElement('h5');
    nome.className = 'fw-bold mb-1';
    nome.textContent = ponto.nome;

    let localizacao = document.createElement('p');
    localizacao.className = 'text-muted mb-1';
    localizacao.innerHTML = `<i class="bi bi-geo-alt-fill"></i> ${ponto.localizacao}`;

    let categoria = document.createElement('p');
    categoria.className = 'mb-1';
    categoria.innerHTML = `<strong>Categoria:</strong> ${ponto.categoria.nome}`;

    let tipo = document.createElement('p');
    tipo.className = 'mb-1';
    let tipoLabel = ponto.tipo_ponto.charAt(0).toUpperCase() + ponto.tipo_ponto.slice(1);
    tipo.innerHTML = `<strong>Tipo:</strong> ${tipoLabel}`;

    textos.appendChild(nome);
    textos.appendChild(localizacao);
    textos.appendChild(categoria);
    textos.appendChild(tipo);

    if (ponto.sugerido_por) {
        let sugeridoPor = document.createElement('p');
        sugeridoPor.className = 'mb-0';
        sugeridoPor.innerHTML = `<strong>Sugerido por:</strong> ${ponto.sugerido_por}`;
        textos.appendChild(sugeridoPor);
    }

    grupoImagem.appendChild(imagem);
    grupoImagem.appendChild(textos);
    colunaInfo.appendChild(grupoImagem);

    let acoes = document.createElement('div');
    acoes.className = 'col-lg-4 text-lg-end mt-3 mt-lg-0';

    let statusEscrita = document.createElement('span');
    statusEscrita.className = 'fs-6 mb-3 badge ';

    if (ponto.status == 'aprovado') {
        statusEscrita.className += 'bg-success';
        statusEscrita.innerHTML = '<i class="bi bi-check-circle-fill"></i> Aprovado';
    } else if (ponto.status == 'rejeitado') {
        statusEscrita.className += 'bg-danger';
        statusEscrita.innerHTML = '<i class="bi bi-x-circle-fill"></i> Rejeitado';
    } else {
        statusEscrita.className += 'bg-warning text-dark';
        statusEscrita.innerHTML = '<i class="bi bi-clock-fill"></i> Pendente';
    }

    let botoes = document.createElement('div');
    botoes.className = 'd-flex justify-content-lg-end justify-content-start gap-2';

    let verDetalhes = document.createElement('a');
    verDetalhes.href = `/detalhes-ponto/${ponto.id}`;
    verDetalhes.className = 'btn btn-primary';
    verDetalhes.title = 'Ver detalhes';
    verDetalhes.innerHTML = '<i class="bi bi-eye-fill"></i>';
    botoes.appendChild(verDetalhes);

    if (ponto.status == 'pendente') {
        let aprovar = document.createElement('button');
        aprovar.type = 'button';
        aprovar.className = 'btn btn-success';
        aprovar.title = 'Aprovar';
        aprovar.innerHTML = '<i class="bi bi-check-lg"></i>';
        aprovar.addEventListener('click', () => alterarStatusSugestao(ponto, 'aprovado'));

        let rejeitar = document.createElement('button');
        rejeitar.type = 'button';
        rejeitar.className = 'btn btn-rejeitar';
        rejeitar.title = 'Rejeitar';
        rejeitar.innerHTML = '<i class="bi bi-x-lg"></i>';
        rejeitar.addEventListener('click', () => alterarStatusSugestao(ponto, 'rejeitado'));

        botoes.appendChild(aprovar);
        botoes.appendChild(rejeitar);
    }

    let excluir = document.createElement('button');
    excluir.type = 'button';
    excluir.className = 'btn btn-danger';
    excluir.title = 'Excluir';
    excluir.innerHTML = '<i class="bi bi-trash-fill"></i>';
    excluir.addEventListener('click', () => removerSugestao(ponto, coluna));

    botoes.appendChild(excluir);

    acoes.appendChild(statusEscrita);
    acoes.appendChild(document.createElement('br'));
    acoes.appendChild(botoes);

    linhaInterna.appendChild(colunaInfo);
    linhaInterna.appendChild(acoes);
    corpoCartao.appendChild(linhaInterna);
    cartao.appendChild(corpoCartao);
    coluna.appendChild(cartao);

    return coluna;
}

async function alterarStatusSugestao(ponto, status) {
    if (status == 'rejeitado') {
        let confirmar = confirm(`Deseja realmente rejeitar a sugestão ${ponto.nome}?`);
        if (!confirmar) {
            return;
        }
    }

    let formData = new FormData();
    formData.append('nome', ponto.nome);
    formData.append('localizacao', ponto.localizacao);
    formData.append('descricao', ponto.descricao);
    formData.append('horario_funcionamento', ponto.horario_funcionamento);
    formData.append('custo_entrada', ponto.custo_entrada);
    formData.append('categoria', ponto.categoria.id);
    formData.append('tipo_ponto', ponto.tipo_ponto);
    formData.append('status', status);

    if (ponto.promocao) {
        formData.append('promocao', ponto.promocao.id);
    }

    if (ponto.tipo_ponto == 'cultural') {
        if (ponto.tipo_cultural) {
            formData.append('tipo_cultural', ponto.tipo_cultural.id);
        }
        formData.append('ano_fundacao', ponto.ano_fundacao);
    } else {
        if (ponto.ecossistema) {
            formData.append('ecossistema', ponto.ecossistema.id);
        }
        formData.append('area_km', ponto.area_km);
    }

    (ponto.destaques || []).forEach(destaque => {
        formData.append('destaques', destaque.id);
    });

    let resposta = await apiFetch(`${API_PONTO_URL}/${ponto.id}`, {
        method: 'PUT',
        body: formData
    });

    let dados = await resposta.json();

    if (resposta.ok) {
        await listarSugestoes();
    }

    mostrarMensagem(dados.mensagem, dados.classe);
}

async function removerSugestao(ponto, coluna) {
    let confirmar = confirm(`Tem certeza que deseja excluir o ponto turístico ${ponto.nome}?`);

    if (!confirmar) {
        return;
    }

    let resposta = await apiFetch(`${API_PONTO_URL}/${ponto.id}`, {
        method: 'DELETE'
    });

    let dados = await resposta.json();

    coluna.remove();

    mostrarMensagem(dados.mensagem, dados.classe);
}