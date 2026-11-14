import { API_AVALIACAO_URL, mostrarMensagem, apiFetch, usuarioModerador, criarBadgeStatus, criarDropdownAcoesAdmin, criarDropdownFiltroStatus } from '../main.js';

const idPonto = window.location.pathname.split('/').filter(Boolean).pop();
let filtroStatusAtual = '';

document.addEventListener('DOMContentLoaded', async () => {
    document.getElementById('btn-voltar').addEventListener('click', () => {
        window.location.href = `/detalhes-ponto/${idPonto}`;
    });
    await carregarAvaliacoes();
});

async function carregarAvaliacoes() {
    let moderador = await usuarioModerador();

    let url = `${API_AVALIACAO_URL}/ponto/${idPonto}`;
    if (!moderador) {
        url += '?status=aprovado';
    } else if (filtroStatusAtual) {
        url += `?status=${filtroStatusAtual}`;
    }

    let resposta = await apiFetch(url);
    let dados = await resposta.json();

    if (!resposta.ok) {
        mostrarMensagem(dados.mensagem, dados.classe);
        return;
    }

    document.getElementById('titulo-avaliacoes').innerHTML = `Avaliações de <strong>${dados.ponto_nome}</strong>`;

    let filtroContainer = document.getElementById('filtro-status-container');
    filtroContainer.innerHTML = '';

    if (moderador) {
        filtroContainer.appendChild(criarDropdownFiltroStatus(filtroStatusAtual, async (valor) => {
            filtroStatusAtual = valor;
            await carregarAvaliacoes();
        }));
    }

    montarAvaliacaoUsuario(dados.avaliacao_usuario, dados.logado);
    montarListaAvaliacoes(dados.avaliacoes, dados.usuario_admin);
}

function formatarData(dataIso) {
    let data = new Date(dataIso);
    let dataFormatada = data.toLocaleDateString('pt-BR');
    let horaFormatada = data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    return `${dataFormatada} ${horaFormatada}`;
}

function criarEstrelas(nota) {
    return '⭐'.repeat(nota);
}

function montarAvaliacaoUsuario(avaliacaoUsuario, logado) {
    let container = document.getElementById('avaliacao-usuario-container');
    container.innerHTML = '';

    if (!logado || !avaliacaoUsuario) return;

    let card = document.createElement('div');
    card.className = 'card shadow-sm mb-3 border-primary';

    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let topo = document.createElement('div');
    topo.className = 'd-flex justify-content-between align-items-start';

    let infoUsuario = document.createElement('div');
    infoUsuario.className = 'd-flex align-items-center mb-2';
    infoUsuario.innerHTML = `
        <img src="/static/${avaliacaoUsuario.usuario.url_foto}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
        <div>
            <strong>${avaliacaoUsuario.usuario.username} (Você)</strong><br>
            <small class="text-muted">${formatarData(avaliacaoUsuario.data_avaliacao)}</small>
        </div>
    `;

    let acoes = document.createElement('div');
    acoes.className = 'd-flex gap-2';

    let botaoEditar = document.createElement('a');
    botaoEditar.href = `/editar-avaliacao/${idPonto}`;
    botaoEditar.className = 'btn btn-warning btn-sm d-flex align-items-center justify-content-center';
    botaoEditar.title = 'Editar';
    botaoEditar.innerHTML = '<i class="bi bi-pencil"></i>';

    let botaoExcluir = document.createElement('button');
    botaoExcluir.className = 'btn btn-danger btn-sm d-flex align-items-center justify-content-center';
    botaoExcluir.title = 'Excluir';
    botaoExcluir.innerHTML = '<i class="bi bi-trash"></i>';
    botaoExcluir.addEventListener('click', () => excluirAvaliacao(avaliacaoUsuario.usuario.email));

    acoes.appendChild(botaoEditar);
    acoes.appendChild(botaoExcluir);
    topo.appendChild(infoUsuario);
    topo.appendChild(acoes);

    let notaLinha = document.createElement('div');
    notaLinha.className = 'd-flex justify-content-between align-items-center mb-1';

    let nota = document.createElement('p');
    nota.className = 'text-warning mb-0';
    nota.textContent = criarEstrelas(avaliacaoUsuario.nota);

    notaLinha.appendChild(nota);
    notaLinha.appendChild(criarBadgeStatus(avaliacaoUsuario.status));

    corpo.appendChild(topo);
    corpo.appendChild(notaLinha);

    if (avaliacaoUsuario.comentario) {
        let comentario = document.createElement('p');
        comentario.textContent = avaliacaoUsuario.comentario;
        corpo.appendChild(comentario);
    }

    card.appendChild(corpo);
    container.appendChild(card);
}

function montarListaAvaliacoes(avaliacoes, usuarioAdmin) {
    let lista = document.getElementById('lista-avaliacoes');
    lista.innerHTML = '';

    if (!avaliacoes || avaliacoes.length == 0) {
        let vazio = document.createElement('div');
        vazio.className = 'alert alert-secondary text-center';
        vazio.textContent = 'Nenhuma avaliação encontrada!';
        lista.appendChild(vazio);
        return;
    }

    avaliacoes.forEach(avaliacao => {
        lista.appendChild(criarCardAvaliacao(avaliacao, usuarioAdmin));
    });
}

function criarCardAvaliacao(avaliacao, usuarioAdmin) {
    let card = document.createElement('div');
    card.className = 'card shadow-sm mb-3';

    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let topo = document.createElement('div');
    topo.className = 'd-flex justify-content-between align-items-start';

    let infoUsuario = document.createElement('div');
    infoUsuario.className = 'd-flex align-items-center mb-2';
    infoUsuario.innerHTML = `
        <img src="/static/${avaliacao.usuario.url_foto}" class="rounded-circle me-2" width="40" height="40" style="object-fit: cover;">
        <div>
            <strong>${avaliacao.usuario.username}</strong><br>
            <small class="text-muted">${formatarData(avaliacao.data_avaliacao)}</small>
        </div>
    `;

    topo.appendChild(infoUsuario);

    if (usuarioAdmin) {
        let acoes = document.createElement('div');
        acoes.className = 'd-flex gap-2';

        if (avaliacao.status == 'pendente') {
            acoes.appendChild(criarDropdownAcoesAdmin(avaliacao, idPonto, carregarAvaliacoes));
        }

        let botaoExcluir = document.createElement('button');
        botaoExcluir.className = 'btn btn-danger btn-sm d-flex align-items-center justify-content-center';
        botaoExcluir.title = 'Excluir';
        botaoExcluir.innerHTML = '<i class="bi bi-trash"></i>';
        botaoExcluir.addEventListener('click', () => excluirAvaliacao(avaliacao.usuario.email, avaliacao.usuario.username));

        acoes.appendChild(botaoExcluir);
        topo.appendChild(acoes);
    }

    let notaLinha = document.createElement('div');
    notaLinha.className = 'd-flex justify-content-between align-items-center mb-1';

    let nota = document.createElement('p');
    nota.className = 'text-warning mb-0';
    nota.textContent = criarEstrelas(avaliacao.nota);

    notaLinha.appendChild(nota);

    if (usuarioAdmin) {
        notaLinha.appendChild(criarBadgeStatus(avaliacao.status));
    }

    corpo.appendChild(topo);
    corpo.appendChild(notaLinha);

    if (avaliacao.comentario) {
        let comentario = document.createElement('p');
        comentario.textContent = avaliacao.comentario;
        corpo.appendChild(comentario);
    }

    card.appendChild(corpo);
    return card;
}

async function excluirAvaliacao(usuarioEmail, username) {
    let mensagem = username
        ? `Tem certeza que deseja excluir a avaliação de ${username}?`
        : 'Tem certeza que deseja excluir sua avaliação?';

    if (!confirm(mensagem)) return;

    let resposta = await apiFetch(`${API_AVALIACAO_URL}/ponto/${idPonto}?usuario_email=${encodeURIComponent(usuarioEmail)}`, {
        method: 'DELETE'
    });

    let dados = await resposta.json();
    mostrarMensagem(dados.mensagem, dados.classe);

    if (resposta.ok) {
        await carregarAvaliacoes();
    }
}