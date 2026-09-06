import { API_USUARIO_URL, criarFaixaDestaques, criarAvaliacao, criarPreco, criarBotaoDetalhes, criarBotaoFavorito, apiFetch } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await listarFavoritos();
});

async function listarFavoritos() {
    let container = document.getElementById('lista-favoritos');
    container.innerHTML = '';

    let resposta = await apiFetch(`${API_USUARIO_URL}/favoritos`);
    let favoritos = await resposta.json();

    if (favoritos.length == 0) {
        mostrarEstadoVazio(container);
        return;
    }

    favoritos.forEach(ponto => {
        ponto.favorito = true;
        container.appendChild(criarCardFavorito(ponto));
    });
}

function mostrarEstadoVazio(container) {
    let alerta = document.createElement('div');
    alerta.className = 'alert alert-secondary text-center';
    alerta.textContent = 'Você ainda não favoritou nenhum ponto turístico.';
    container.appendChild(alerta);
}

function criarCardFavorito(ponto) {
    let coluna = document.createElement('div');
    coluna.className = 'col-md-4 mb-4 d-flex';

    let card = document.createElement('div');
    card.className = 'card shadow-sm card-hover card-ponto w-100 position-relative';

    let topo = document.createElement('div');
    topo.className = 'position-relative';

    if (ponto.promocao) {
        let badgeDesconto = document.createElement('div');
        badgeDesconto.className = 'badge-desconto';
        badgeDesconto.textContent = `-${Math.trunc(Number(ponto.promocao.desconto))}%`;
        topo.appendChild(badgeDesconto);
    }

    let imagem = document.createElement('img');
    imagem.src = `/static/${ponto.url_imagem}`;
    imagem.className = 'card-img-top rounded-top';
    imagem.style.height = '300px';
    imagem.style.objectFit = 'cover';
    topo.appendChild(imagem);

    if (ponto.destaques && ponto.destaques.length > 0) {
        topo.appendChild(criarFaixaDestaques(ponto.destaques));
    }

    card.appendChild(topo);

    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let info = document.createElement('div');

    let nome = document.createElement('h5');
    nome.textContent = ponto.nome;
    info.appendChild(nome);

    let tipo = document.createElement('p');
    tipo.className = 'text-muted';
    let tipoLabel = ponto.tipo_ponto.charAt(0).toUpperCase() + ponto.tipo_ponto.slice(1);
    tipo.textContent = `Ponto ${tipoLabel}`;
    info.appendChild(tipo);

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

    let botaoFavorito = criarBotaoFavorito(ponto, (favorito) => {
        if (!favorito) {
            coluna.remove();

            let container = document.getElementById('lista-favoritos');
            if (container.querySelectorAll('.card').length == 0) {
                mostrarEstadoVazio(container);
            }
        }
    });
    linhaPreco.appendChild(botaoFavorito);

    corpo.appendChild(info);
    corpo.appendChild(linhaPreco);
    corpo.appendChild(criarBotaoDetalhes(ponto));

    card.appendChild(corpo);
    coluna.appendChild(card);

    return coluna;
}