import { API_PONTO_URL, API_CATEGORIA_URL, criarBotaoFavorito, apiFetch } from '../main.js';

let paginaAtual = 1;

document.addEventListener('DOMContentLoaded', async () => {
    await carregarCategorias();
    await listarPontosAprovados();

    document.getElementById('form-filtro-pontos').addEventListener('submit', async (evento) => {
        evento.preventDefault();
        paginaAtual = 1;
        await listarPontosAprovados();
    });
});

async function carregarCategorias() {
    let resposta = await apiFetch(API_CATEGORIA_URL);
    let categorias = await resposta.json();

    let select = document.getElementById('filtro-categoria');

    categorias.forEach(categoria => {
        let option = document.createElement('option');
        option.value = categoria.nome;
        option.textContent = categoria.nome;
        select.appendChild(option);
    });
}

function montarQueryString() {
    let busca = document.getElementById('filtro-busca').value.trim();
    let categoria = document.getElementById('filtro-categoria').value;
    let tipo = document.getElementById('filtro-tipo').value;
    let localizacao = document.getElementById('filtro-localizacao').value.trim();

    let parametros = new URLSearchParams();
    parametros.set('status', 'aprovado');
    parametros.set('page', paginaAtual);
    parametros.set('limit', 9);

    if (busca) parametros.set('busca', busca);
    if (categoria) parametros.set('categoria', categoria);
    if (tipo) parametros.set('tipo', tipo);
    if (localizacao) parametros.set('localizacao', localizacao);

    return parametros.toString();
}

async function listarPontosAprovados() {
    let container = document.getElementById('lista-pontos-aprovados');
    container.innerHTML = '';

    let queryString = montarQueryString();
    let resposta = await apiFetch(`${API_PONTO_URL}?${queryString}`);
    let dados = await resposta.json();

    let logado = dados.logado;
    let pontos = dados.pontos;

    if (pontos.length == 0) {
        let alerta = document.createElement('div');
        alerta.className = 'alert alert-secondary text-center';
        alerta.textContent = 'Nenhum ponto turístico encontrado.';
        container.appendChild(alerta);
        renderizarPaginacao(dados.paginacao);
        return;
    }

    pontos.forEach(ponto => {
        container.appendChild(criarCardPonto(ponto, logado));
    });

    renderizarPaginacao(dados.paginacao);
}

function renderizarPaginacao(paginacao) {
    let nav = document.getElementById('paginacao-pontos');
    nav.innerHTML = '';

    if (!paginacao || paginacao.total_paginas <= 1) {
        return;
    }

    let lista = document.createElement('ul');
    lista.className = 'pagination justify-content-center';

    for (let pagina = 1; pagina <= paginacao.total_paginas; pagina++) {
        let item = document.createElement('li');
        item.className = `page-item ${pagina == paginacao.page ? 'active' : ''}`;

        let link = document.createElement('a');
        link.className = 'page-link';
        link.href = '#';
        link.textContent = pagina;

        link.addEventListener('click', async (evento) => {
            evento.preventDefault();
            paginaAtual = pagina;
            await listarPontosAprovados();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        item.appendChild(link);
        lista.appendChild(item);
    }

    nav.appendChild(lista);
}

function criarCardPonto(ponto, logado) {
    let coluna = document.createElement('div');
    coluna.className = 'col-md-4 mb-4 d-flex';

    let card = document.createElement('div');
    card.className = 'card shadow-sm card-hover card-ponto w-100 position-relative';

    let topo = document.createElement('div');
    topo.className = 'position-relative';

    let imagem = document.createElement('img');
    imagem.src = `/static/${ponto.url_imagem}`;
    imagem.className = 'card-img-top rounded-top ponto-img';
    imagem.style.height = '300px';
    imagem.style.objectFit = 'cover';

    topo.appendChild(imagem);

    if (ponto.destaques && ponto.destaques.length > 0) {
        let faixaDestaques = document.createElement('div');
        faixaDestaques.className = 'position-absolute bottom-0 start-0 w-100 p-2 d-flex flex-wrap gap-1';
        faixaDestaques.style.background = 'linear-gradient(to top, rgba(0,0,0,0.6), transparent)';

        ponto.destaques.forEach(destaque => {
            let badge = document.createElement('span');
            badge.className = 'badge bg-dark bg-opacity-75 text-white';
            badge.textContent = `#${destaque.nome}`;
            faixaDestaques.appendChild(badge);
        });

        topo.appendChild(faixaDestaques);
    }

    if (ponto.promocao) {
        let badgeDesconto = document.createElement('div');
        badgeDesconto.className = 'badge-desconto';
        badgeDesconto.textContent = `-${Math.trunc(Number(ponto.promocao.desconto))}%`;
        topo.appendChild(badgeDesconto);
    }

    card.appendChild(topo);

    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let infoTopo = document.createElement('div');

    let nome = document.createElement('h5');
    nome.textContent = ponto.nome;

    let tipo = document.createElement('p');
    tipo.className = 'text-muted';
    let tipoLabel = ponto.tipo_ponto.charAt(0).toUpperCase() + ponto.tipo_ponto.slice(1);
    tipo.textContent = `Ponto ${tipoLabel}`;

    let localizacao = document.createElement('p');
    localizacao.className = 'text-muted localizacao';
    localizacao.textContent = ponto.localizacao;

    let categoria = document.createElement('p');
    categoria.className = 'text-muted';
    categoria.textContent = ponto.categoria.nome;

    let avaliacao = document.createElement('p');
    avaliacao.className = 'text-warning';
    let media = ponto.media_avaliacao !== null && ponto.media_avaliacao !== undefined ? Number(ponto.media_avaliacao) : null;
    if (media !== null) {
        avaliacao.textContent = `⭐ ${media.toFixed(1)}`;
    } else {
        avaliacao.textContent = '⭐ Nenhuma avaliação';
    }

    infoTopo.appendChild(nome);
    infoTopo.appendChild(tipo);
    infoTopo.appendChild(localizacao);
    infoTopo.appendChild(categoria);
    infoTopo.appendChild(avaliacao);

    let linhaPreco = document.createElement('div');
    linhaPreco.className = 'd-flex justify-content-between align-items-center';

    let preco = document.createElement('p');
    preco.className = 'preco mb-0';

    let custoEntrada = Number(ponto.custo_entrada);

    if (custoEntrada) {
        if (ponto.promocao) {
            let precoAntigo = document.createElement('span');
            precoAntigo.className = 'preco-antigo';
            precoAntigo.textContent = `R$ ${custoEntrada.toFixed(2)}`;

            let valorComDesconto = custoEntrada * (1 - Number(ponto.promocao.desconto) / 100);

            let precoPromocao = document.createElement('span');
            precoPromocao.className = 'preco-promocao';
            precoPromocao.textContent = `R$ ${valorComDesconto.toFixed(2)}`;

            preco.appendChild(precoAntigo);
            preco.appendChild(precoPromocao);
        } else {
            preco.textContent = `R$ ${custoEntrada.toFixed(2)}`;
        }
    } else {
        let precoGratuito = document.createElement('span');
        precoGratuito.className = 'preco-promocao';
        precoGratuito.textContent = 'Gratuito';
        preco.appendChild(precoGratuito);
    }

    linhaPreco.appendChild(preco);

    if (logado) {
        linhaPreco.appendChild(criarBotaoFavorito(ponto));
    }

    corpo.appendChild(infoTopo);
    corpo.appendChild(linhaPreco);

    let botaoDetalhes = document.createElement('a');
    botaoDetalhes.href = `/detalhes-ponto/${ponto.id}`;
    botaoDetalhes.className = 'btn btn-primary w-100 mt-2';
    botaoDetalhes.textContent = 'Ver detalhes';

    corpo.appendChild(botaoDetalhes);

    card.appendChild(corpo);
    coluna.appendChild(card);

    return coluna;
}