import { mostrarMensagem, API_REDEFINICAO_URL, apiFetch } from '../main.js';

document.addEventListener('DOMContentLoaded', () => {
    let olho1 = document.getElementById('eye-reset_senha');
    let olho2 = document.getElementById('eye-reset_confirmar_senha');
    olho1.src = '/static/img/default/open_eye.svg';
    olho2.src = '/static/img/default/open_eye.svg';

    document.getElementById('form-redefinir-senha').addEventListener('submit', redefinirSenha);
});

async function redefinirSenha(evento) {
    evento.preventDefault();

    let form = document.getElementById('form-redefinir-senha');
    let token = form.dataset.token;
    let dados = {
        'senha': form.senha.value,
        'confirmar_senha': form.confirmar_senha.value
    }

    let resposta = await apiFetch(`${API_REDEFINICAO_URL}/${token}`, {
        method: 'POST',
        body: JSON.stringify(dados),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    let dadosResp = await resposta.json();

    if (resposta.ok) {
        sessionStorage.setItem('mensagemPendente', JSON.stringify({
            mensagem: dadosResp.mensagem,
            classe: dadosResp.classe
        }));

        window.location.href = '/login';
    }
    else {
        mostrarMensagem(dadosResp.mensagem, dadosResp.classe);
    }
}