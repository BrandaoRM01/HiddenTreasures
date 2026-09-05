import { mostrarMensagem, API_RECUPERACAO_URL } from '../main.js';

document.addEventListener('DOMContentLoaded', () => {
    let voltarLogin = document.getElementById('voltar');
    voltarLogin.href = '/login';

    document.getElementById('form-recuperar-senha').addEventListener('submit', enviarRecuperacao);
});

async function enviarRecuperacao(evento) {
    evento.preventDefault();

    let form = document.getElementById('form-recuperar-senha');
    let dados = {
        'email': form.email.value
    };

    let resposta = await fetch(API_RECUPERACAO_URL, {
        method: 'POST',
        body: JSON.stringify(dados),
        headers: {
            'Content-Type': 'application/json'
        }
    });

    let dadosResp = await resposta.json();

    if (resposta.ok) {
        form.reset();
    }

    mostrarMensagem(dadosResp.mensagem, dadosResp.classe);
}