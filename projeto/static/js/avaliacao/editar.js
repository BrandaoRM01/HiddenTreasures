import { API_AVALIACAO_URL, inicializarEstrelas, mostrarMensagem } from '../main.js';

const idPonto = window.location.pathname.split('/').filter(Boolean).pop();

document.addEventListener('DOMContentLoaded', async () => {
    const formEditar = document.getElementById('form-editar');
    const voltar = document.getElementById('voltar');
    voltar.href = `/detalhes-ponto/${idPonto}`;

    let resposta = await fetch(`${API_AVALIACAO_URL}/ponto/${idPonto}`);
    let dados = await resposta.json();

    if (!resposta.ok || !dados.avaliacao_usuario) {
        mostrarMensagem('Avaliação não encontrada.', 'danger');
        window.location.href = `/detalhes-ponto/${idPonto}`;
        return;
    }

    montarTitulo(dados.ponto_nome);
    montarEstrelas(dados.avaliacao_usuario.nota);

    document.getElementById('comentario').value = dados.avaliacao_usuario.comentario || '';

    formEditar.addEventListener('submit', enviarEdicao);
});

function montarTitulo(pontoNome) {
    let titulo = document.getElementById('titulo-editar');
    titulo.innerHTML = '';

    let forte = document.createElement('strong');
    forte.textContent = pontoNome;

    titulo.appendChild(document.createTextNode('Editar Avaliação de '));
    titulo.appendChild(forte);
}

function montarEstrelas(notaAtual) {
    let container = document.getElementById('stars-container');
    container.innerHTML = '';

    for (let valor = 1; valor <= 5; valor++) {
        let estrela = document.createElement('i');
        estrela.className = 'star';
        estrela.setAttribute('data-value', valor);
        estrela.textContent = '★';

        if (valor <= notaAtual) {
            estrela.classList.add('active');
        }

        container.appendChild(estrela);
    }

    document.getElementById('nota').value = notaAtual;

    inicializarEstrelas();
}

async function enviarEdicao(evento) {
    evento.preventDefault();

    let nota = document.getElementById('nota').value;
    let comentario = document.getElementById('comentario').value;

    if (!nota) {
        mostrarMensagem('Selecione uma nota antes de salvar.', 'danger');
        return;
    }

    let resposta = await fetch(`${API_AVALIACAO_URL}/ponto/${idPonto}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nota, comentario })
    });

    let dados = await resposta.json();
    mostrarMensagem(dados.mensagem, dados.classe);
}