import { API_PONTO_URL, API_AVALIACAO_URL, inicializarEstrelas, mostrarMensagem } from '../main.js';

const idPonto = window.location.pathname.split('/').filter(Boolean).pop();

document.addEventListener('DOMContentLoaded', async () => {
    await carregarPonto();
    await carregarAvaliacoesPreview();
});

async function carregarPonto() {
    let resposta = await fetch(`${API_PONTO_URL}/detalhes/${idPonto}`);
    let ponto = await resposta.json();

    if (!resposta.ok) {
        window.location.href = '/pontos';
        return;
    }

    montarImagem(ponto);
    montarInfo(ponto);
    montarSecaoAvaliar(ponto);
}

function montarImagem(ponto) {
    let container = document.getElementById('imagem-container');
    container.innerHTML = '';

    if (ponto.promocao) {
        let badge = document.createElement('span');
        badge.style.position = 'absolute';
        badge.style.top = '10px';
        badge.style.left = '10px';
        badge.style.backgroundColor = '#d63384';
        badge.style.color = 'white';
        badge.style.padding = '5px 10px';
        badge.style.borderRadius = '8px';
        badge.style.fontWeight = 'bold';
        badge.style.zIndex = '2';
        badge.textContent = `-${Math.trunc(Number(ponto.promocao.desconto))}%`;
        container.appendChild(badge);
    }

    let imagem = document.createElement('img');
    imagem.src = `/static/${ponto.url_imagem}`;
    imagem.className = 'img-fluid';
    container.appendChild(imagem);

    if (ponto.destaques && ponto.destaques.length > 0) {
        let faixa = document.createElement('div');
        faixa.className = 'position-absolute bottom-0 start-0 w-100 p-2 d-flex flex-wrap gap-1';
        faixa.style.background = 'linear-gradient(to top, rgba(0,0,0,0.65), transparent)';

        ponto.destaques.forEach(d => {
            let badgeDestaque = document.createElement('span');
            badgeDestaque.className = 'badge bg-dark bg-opacity-75 text-white';
            badgeDestaque.textContent = `#${d.nome}`;
            faixa.appendChild(badgeDestaque);
        });

        container.appendChild(faixa);
    }
}

function criarParagrafo(rotulo, valor) {
    let p = document.createElement('p');
    let forte = document.createElement('strong');
    forte.textContent = `${rotulo}: `;
    p.appendChild(forte);
    p.appendChild(document.createTextNode(valor));
    return p;
}

function capitalizar(texto) {
    return texto.charAt(0).toUpperCase() + texto.slice(1);
}

function formatarDataSimples(dataIso) {
    return new Date(dataIso).toLocaleDateString('pt-BR');
}

function criarBlocoPromocao(promocao, custoEntrada) {
    let bloco = document.createElement('div');
    bloco.className = 'mt-2 p-3';
    bloco.style.backgroundColor = '#f8f9fa';
    bloco.style.borderLeft = '4px solid #d63384';
    bloco.style.borderRadius = '8px';

    let titulo = document.createElement('h5');
    titulo.className = 'mb-1';
    let tituloForte = document.createElement('strong');
    tituloForte.textContent = promocao.titulo;
    titulo.appendChild(tituloForte);

    let descricao = document.createElement('p');
    descricao.className = 'mb-1';
    descricao.textContent = promocao.descricao || 'Sem descrição';

    let validade = document.createElement('p');
    validade.style.fontSize = '0.9rem';
    validade.style.color = '#555';
    validade.style.marginTop = '4px';
    validade.textContent = `Promoção válida de ${formatarDataSimples(promocao.data_inicio)} até ${formatarDataSimples(promocao.data_fim)}`;

    let precoLinha = document.createElement('p');
    precoLinha.className = 'mb-0';

    if (custoEntrada) {
        let valorComDesconto = custoEntrada * (1 - Number(promocao.desconto) / 100);

        let precoAntigo = document.createElement('span');
        precoAntigo.style.textDecoration = 'line-through';
        precoAntigo.style.color = '#999';
        precoAntigo.textContent = `R$ ${custoEntrada.toFixed(2)}`;

        let precoNovo = document.createElement('span');
        precoNovo.style.color = '#d63384';
        precoNovo.style.fontWeight = 'bold';
        precoNovo.textContent = ` R$ ${valorComDesconto.toFixed(2)}`;

        precoLinha.appendChild(precoAntigo);
        precoLinha.appendChild(precoNovo);
    } else {
        let gratuito = document.createElement('span');
        gratuito.style.color = '#d63384';
        gratuito.style.fontWeight = 'bold';
        gratuito.textContent = 'Gratuito';
        precoLinha.appendChild(gratuito);
    }

    bloco.appendChild(titulo);
    bloco.appendChild(descricao);
    bloco.appendChild(validade);
    bloco.appendChild(precoLinha);

    return bloco;
}

function montarInfo(ponto) {
    let container = document.getElementById('info-ponto');
    container.innerHTML = '';

    let nomeTitulo = document.createElement('h2');
    let nomeForte = document.createElement('strong');
    nomeForte.textContent = ponto.nome;
    nomeTitulo.appendChild(nomeForte);
    container.appendChild(nomeTitulo);

    container.appendChild(criarParagrafo('Tipo', `Ponto ${capitalizar(ponto.tipo_ponto)}`));
    container.appendChild(criarParagrafo('Localização', ponto.localizacao));
    container.appendChild(criarParagrafo('Descrição', ponto.descricao));

    if (ponto.horario_funcionamento) {
        container.appendChild(criarParagrafo('Horário de Funcionamento', ponto.horario_funcionamento));
    }

    container.appendChild(criarParagrafo('Categoria', ponto.categoria.nome));

    if (ponto.tipo_ponto === 'cultural') {
        container.appendChild(criarParagrafo('Tipo Cultural', ponto.tipo_cultural ? ponto.tipo_cultural.nome : 'Não especificado'));
        container.appendChild(criarParagrafo('Ano de Fundação', ponto.ano_fundacao || 'Não informado'));
    } else if (ponto.tipo_ponto === 'natural') {
        container.appendChild(criarParagrafo('Ecossistema', ponto.ecossistema ? ponto.ecossistema.nome : 'Não especificado'));
        container.appendChild(criarParagrafo('Área', ponto.area_km ? `${ponto.area_km} km²` : 'Não informada'));
    }

    let custoEntrada = Number(ponto.custo_entrada);

    if (ponto.promocao) {
        container.appendChild(criarBlocoPromocao(ponto.promocao, custoEntrada));
    } else {
        container.appendChild(criarParagrafo('Custo de Entrada', custoEntrada > 0 ? `R$ ${custoEntrada.toFixed(2)}` : 'Gratuito'));
    }
}

function montarSecaoAvaliar(ponto) {
    let container = document.getElementById('secao-avaliar');
    container.innerHTML = '';

    if (ponto.status !== 'aprovado') return;

    if (!ponto.logado) {
        let alerta = document.createElement('div');
        alerta.className = 'alert alert-info text-center mb-4';

        let link = document.createElement('a');
        link.className = 'alert-link';
        link.href = '/login';
        link.textContent = 'login';

        alerta.appendChild(document.createTextNode('Faça '));
        alerta.appendChild(link);
        alerta.appendChild(document.createTextNode(' para avaliar este lugar.'));

        container.appendChild(alerta);
        return;
    }

    let card = document.createElement('div');
    card.className = 'card shadow-sm mb-4';

    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let titulo = document.createElement('h5');
    titulo.className = 'mb-3';
    titulo.textContent = 'Avaliar este lugar';

    let form = document.createElement('form');
    form.id = 'form-avaliar';

    let grupoNota = document.createElement('div');
    grupoNota.className = 'mb-3';

    let rotuloNota = document.createElement('label');
    rotuloNota.className = 'form-label';
    rotuloNota.textContent = 'Nota ';

    let obrigatorio = document.createElement('span');
    obrigatorio.className = 'text-danger';
    obrigatorio.textContent = '*';
    rotuloNota.appendChild(obrigatorio);

    let estrelas = document.createElement('div');
    estrelas.className = 'stars';

    for (let valor = 1; valor <= 5; valor++) {
        let estrela = document.createElement('i');
        estrela.className = 'star';
        estrela.setAttribute('data-value', valor);
        estrela.textContent = '★';
        estrelas.appendChild(estrela);
    }

    let notaInput = document.createElement('input');
    notaInput.type = 'hidden';
    notaInput.id = 'nota';
    notaInput.required = true;

    grupoNota.appendChild(rotuloNota);
    grupoNota.appendChild(estrelas);
    grupoNota.appendChild(notaInput);

    let grupoComentario = document.createElement('div');
    grupoComentario.className = 'mb-3';

    let rotuloComentario = document.createElement('label');
    rotuloComentario.className = 'form-label';
    rotuloComentario.textContent = 'Comentário';

    let textarea = document.createElement('textarea');
    textarea.id = 'comentario';
    textarea.className = 'form-control';
    textarea.rows = 3;
    textarea.placeholder = 'Compartilhe sua experiência...';

    grupoComentario.appendChild(rotuloComentario);
    grupoComentario.appendChild(textarea);

    let botaoEnviar = document.createElement('button');
    botaoEnviar.type = 'submit';
    botaoEnviar.className = 'btn btn-primary';
    botaoEnviar.textContent = 'Enviar avaliação';

    form.appendChild(grupoNota);
    form.appendChild(grupoComentario);
    form.appendChild(botaoEnviar);

    corpo.appendChild(titulo);
    corpo.appendChild(form);
    card.appendChild(corpo);
    container.appendChild(card);

    inicializarEstrelas();
    form.addEventListener('submit', enviarAvaliacao);
}

async function enviarAvaliacao(evento) {
    evento.preventDefault();

    let nota = document.getElementById('nota').value;
    let comentario = document.getElementById('comentario').value;

    if (!nota) {
        mostrarMensagem('Selecione uma nota antes de enviar.', 'danger');
        return;
    }

    let resposta = await fetch(`${API_AVALIACAO_URL}/ponto/${idPonto}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nota, comentario })
    });

    let dados = await resposta.json();
    mostrarMensagem(dados.mensagem, dados.classe);

    if (resposta.ok) {
        await carregarAvaliacoesPreview();
        await carregarPonto();
    }
}

function formatarData(dataIso) {
    let data = new Date(dataIso);
    return `${data.toLocaleDateString('pt-BR')} ${data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })}`;
}

function criarEstrelasTexto(nota) {
    return '⭐'.repeat(nota);
}

async function carregarAvaliacoesPreview() {
    let resposta = await fetch(`${API_AVALIACAO_URL}/ponto/${idPonto}`);
    let dados = await resposta.json();

    if (!resposta.ok) return;

    let container = document.getElementById('secao-avaliacoes-preview');
    container.innerHTML = '';

    let quantidade = dados.avaliacoes.length + (dados.avaliacao_usuario ? 1 : 0);

    let cabecalho = document.createElement('div');
    cabecalho.className = 'mb-3 d-flex justify-content-between align-items-center';

    let titulo = document.createElement('h4');
    titulo.className = 'fw-bold';
    titulo.textContent = 'Avaliações';
    cabecalho.appendChild(titulo);

    if (quantidade >= 5) {
        let link = document.createElement('a');
        link.href = `/avaliacoes-ponto/${idPonto}`;
        link.className = 'btn btn-outline-primary btn-sm';
        link.textContent = 'Ver mais';
        cabecalho.appendChild(link);
    }

    container.appendChild(cabecalho);

    if (dados.avaliacao_usuario) {
        container.appendChild(criarCardAvaliacaoUsuario(dados.avaliacao_usuario));
    }

    let preview = dados.avaliacoes.slice(0, 5);

    if (preview.length === 0 && !dados.avaliacao_usuario) {
        let vazio = document.createElement('div');
        vazio.className = 'alert alert-secondary text-center';
        vazio.textContent = 'Nenhuma avaliação ainda. Seja o primeiro!';
        container.appendChild(vazio);
        return;
    }

    preview.forEach(avaliacao => {
        container.appendChild(criarCardAvaliacao(avaliacao, dados.usuario_admin));
    });
}

function criarInfoUsuario(usuario, dataIso, souVoce) {
    let info = document.createElement('div');
    info.className = 'd-flex align-items-center mb-2';

    let imagem = document.createElement('img');
    imagem.src = `/static/${usuario.url_foto}`;
    imagem.className = 'rounded-circle me-2';
    imagem.width = 40;
    imagem.height = 40;
    imagem.style.objectFit = 'cover';

    let textos = document.createElement('div');

    let nome = document.createElement('strong');
    nome.textContent = souVoce ? `${usuario.username} (Você)` : usuario.username;

    let data = document.createElement('small');
    data.className = 'text-muted';
    data.textContent = formatarData(dataIso);

    textos.appendChild(nome);
    textos.appendChild(document.createElement('br'));
    textos.appendChild(data);

    info.appendChild(imagem);
    info.appendChild(textos);

    return info;
}

function criarCardAvaliacaoUsuario(avaliacaoUsuario) {
    let card = document.createElement('div');
    card.className = 'card shadow-sm mb-3 border-primary';

    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let topo = document.createElement('div');
    topo.className = 'd-flex justify-content-between align-items-start';

    let acoes = document.createElement('div');
    acoes.className = 'd-flex gap-2';

    let botaoEditar = document.createElement('a');
    botaoEditar.href = `/editar-avaliacao/${idPonto}`;
    botaoEditar.className = 'btn btn-warning btn-sm d-flex align-items-center justify-content-center';
    botaoEditar.title = 'Editar';

    let iconeEditar = document.createElement('i');
    iconeEditar.className = 'bi bi-pencil';
    botaoEditar.appendChild(iconeEditar);

    let botaoExcluir = document.createElement('button');
    botaoExcluir.className = 'btn btn-danger btn-sm d-flex align-items-center justify-content-center';
    botaoExcluir.title = 'Excluir';

    let iconeExcluir = document.createElement('i');
    iconeExcluir.className = 'bi bi-trash';
    botaoExcluir.appendChild(iconeExcluir);
    botaoExcluir.addEventListener('click', () => excluirAvaliacao(avaliacaoUsuario.usuario.email));

    acoes.appendChild(botaoEditar);
    acoes.appendChild(botaoExcluir);

    topo.appendChild(criarInfoUsuario(avaliacaoUsuario.usuario, avaliacaoUsuario.data_avaliacao, true));
    topo.appendChild(acoes);

    let nota = document.createElement('p');
    nota.className = 'text-warning mb-1';
    nota.textContent = criarEstrelasTexto(avaliacaoUsuario.nota);

    corpo.appendChild(topo);
    corpo.appendChild(nota);

    if (avaliacaoUsuario.comentario) {
        let comentario = document.createElement('p');
        comentario.textContent = avaliacaoUsuario.comentario;
        corpo.appendChild(comentario);
    }

    card.appendChild(corpo);
    return card;
}

function criarCardAvaliacao(avaliacao, usuarioAdmin) {
    let card = document.createElement('div');
    card.className = 'card shadow-sm mb-3';

    let corpo = document.createElement('div');
    corpo.className = 'card-body';

    let topo = document.createElement('div');
    topo.className = 'd-flex justify-content-between align-items-start';

    topo.appendChild(criarInfoUsuario(avaliacao.usuario, avaliacao.data_avaliacao, false));

    if (usuarioAdmin) {
        let botaoExcluir = document.createElement('button');
        botaoExcluir.className = 'btn btn-danger btn-sm d-flex align-items-center justify-content-center';
        botaoExcluir.title = 'Excluir';

        let iconeExcluir = document.createElement('i');
        iconeExcluir.className = 'bi bi-trash';
        botaoExcluir.appendChild(iconeExcluir);
        botaoExcluir.addEventListener('click', () => excluirAvaliacao(avaliacao.usuario.email, avaliacao.usuario.username));

        topo.appendChild(botaoExcluir);
    }

    let nota = document.createElement('p');
    nota.className = 'text-warning mb-1';
    nota.textContent = criarEstrelasTexto(avaliacao.nota);

    corpo.appendChild(topo);
    corpo.appendChild(nota);

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

    let resposta = await fetch(`${API_AVALIACAO_URL}/ponto/${idPonto}?usuario_email=${encodeURIComponent(usuarioEmail)}`, {
        method: 'DELETE'
    });

    let dados = await resposta.json();
    mostrarMensagem(dados.mensagem, dados.classe);

    if (resposta.ok) {
        await carregarAvaliacoesPreview();
    }
}