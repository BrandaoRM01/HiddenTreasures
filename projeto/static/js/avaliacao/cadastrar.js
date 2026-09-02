import { API_AVALIACAO_URL, mostrarMensagem, inicializarEstrelas } from '../main.js';
import { carregarAvaliacoes } from '../ponto_turistico/detalhes_ponto.js';

const idPonto = window.location.pathname.split('/').filter(Boolean).pop();

export function montarSecaoAvaliar(ponto) {
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
        await carregarAvaliacoes();
    }
}