import { API_PONTO_URL, criarFaixaDestaques, criarAvaliacao, criarPreco, criarBotaoDetalhes, criarBotaoFavorito, apiFetch } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await carregarIndex();
});

async function carregarIndex() {
    let resposta = await apiFetch(`${API_PONTO_URL}/index`);
    let dados = await resposta.json();

    montarTopPontos(dados.top_pontos, dados.logado);
    montarPontosPromocao(dados.pontos_promocao, dados.logado);
}

function montarTopPontos(topPontos, logado) {
    let secao = document.getElementById('secao-top-pontos');
    secao.innerHTML = '';

    if (!topPontos || topPontos.length == 0) {
        return;
    }

    let titulo = document.createElement('div');
    titulo.className = 'secao-titulo text-center';
    titulo.innerHTML = '<h3>Pontos Melhores Avaliados</h3>';

    let linha = document.createElement('div');
    linha.className = 'row mb-5';

    topPontos.forEach((ponto, indice) => {
        linha.appendChild(criarCardTopPonto(ponto, indice + 1, logado));
    });

    secao.appendChild(titulo);
    secao.appendChild(linha);
}

function montarPontosPromocao(pontosPromocao, logado) {
    let secao = document.getElementById('secao-pontos-promocao');
    secao.innerHTML = '';

    if (!pontosPromocao || pontosPromocao.length == 0) {
        return;
    }

    let titulo = document.createElement('div');
    titulo.className = 'secao-titulo text-center';
    titulo.innerHTML = '<h3>Pontos em Promoção</h3>';

    let linha = document.createElement('div');
    linha.className = 'row';

    pontosPromocao.forEach(ponto => {
        linha.appendChild(criarCardPromocao(ponto, logado));
    });

    secao.appendChild(titulo);
    secao.appendChild(linha);
}

function classeRanking(posicao) {
    if (posicao == 1) return 'gold';
    if (posicao == 2) return 'silver';
    if (posicao == 3) return 'bronze';
    return 'blue';
}

function criarCardTopPonto(ponto, posicao, logado) {
    let coluna = document.createElement('div');
    coluna.className = 'col-md-4 mb-4 d-flex';

    let card = document.createElement('div');
    card.className = 'card shadow-sm card-hover card-ponto w-100 position-relative';

    if (logado) {
        let favoritoTopo = criarBotaoFavorito(ponto);
        favoritoTopo.classList.add('position-absolute', 'bottom-50', 'start-0', 'm-2');
        favoritoTopo.style.width = '45px';
        favoritoTopo.style.height = '45px';
        card.appendChild(favoritoTopo);
    }

    let numeroRankingTopo = document.createElement('div');
    numeroRankingTopo.className = `ranking-number ${classeRanking(posicao)}`;
    numeroRankingTopo.textContent = posicao;
    card.appendChild(numeroRankingTopo);

    if (ponto.promocao) {
        let badgeDesconto = document.createElement('div');
        badgeDesconto.className = 'badge-desconto-direita';
        badgeDesconto.textContent = `-${Math.trunc(Number(ponto.promocao.desconto))}%`;
        card.appendChild(badgeDesconto);
    }

    let topo = document.createElement('div');
    topo.className = 'position-relative';

    let imagem = document.createElement('img');
    imagem.src = `/static/${ponto.url_imagem}`;
    imagem.className = 'card-img-top rounded-top ponto-img';
    imagem.style.height = '300px';
    imagem.style.objectFit = 'cover';
    topo.appendChild(imagem);

    let numeroRankingImagem = document.createElement('div');
    numeroRankingImagem.className = `ranking-number ${classeRanking(posicao)}`;
    numeroRankingImagem.textContent = posicao;
    topo.appendChild(numeroRankingImagem);

    if (ponto.destaques && ponto.destaques.length > 0) {
        topo.appendChild(criarFaixaDestaques(ponto.destaques));
    }

    card.appendChild(topo);
    card.appendChild(criarCorpoCard(ponto, logado));

    coluna.appendChild(card);
    return coluna;
}

function criarCardPromocao(ponto, logado) {
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
        topo.appendChild(criarFaixaDestaques(ponto.destaques));
    }

    if (ponto.promocao) {
        let badgeDesconto = document.createElement('div');
        badgeDesconto.className = 'badge-desconto';
        badgeDesconto.textContent = `-${Math.trunc(Number(ponto.promocao.desconto))}%`;
        topo.appendChild(badgeDesconto);
    }

    card.appendChild(topo);
    card.appendChild(criarCorpoCard(ponto, logado));

    coluna.appendChild(card);
    return coluna;
}

function criarCorpoCard(ponto, logado) {
    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let info = document.createElement('div');

    let nome = document.createElement('h5');
    nome.textContent = ponto.nome;
    info.appendChild(nome);

    let localizacao = document.createElement('p');
    localizacao.className = 'text-muted localizacao';
    localizacao.textContent = ponto.localizacao;
    info.appendChild(localizacao);

    let categoria = document.createElement('p');
    categoria.className = 'text-muted';
    categoria.textContent = ponto.categoria.nome;
    info.appendChild(categoria);

    info.appendChild(criarAvaliacao(ponto));

    let linhaPreco = document.createElement('div');
    linhaPreco.className = 'd-flex justify-content-between align-items-center';
    linhaPreco.appendChild(criarPreco(ponto));

    if (logado) {
        linhaPreco.appendChild(criarBotaoFavorito(ponto));
    }

    corpo.appendChild(info);
    corpo.appendChild(linhaPreco);
    corpo.appendChild(criarBotaoDetalhes(ponto));

    return corpo;
}