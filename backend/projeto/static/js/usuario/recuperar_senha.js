import { mostrarMensagem, API_RECUPERACAO_URL, apiFetch, protegerRota } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    let podeAcessar = await protegerRota('visitante');
    if (!podeAcessar) return;

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

    let resposta = await apiFetch(API_RECUPERACAO_URL, {
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