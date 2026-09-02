import { API_PONTO_URL, API_USUARIO_URL, mostrarMensagem } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    let formLogin = document.getElementById('form-login');

    let cadastro = document.getElementById('cadastro');
    cadastro.href = '/cadastro';

    let esqueceu_senha = document.getElementById('esqueceu_senha');
    esqueceu_senha.href = '/recuperar-senha';

    let olho = document.getElementById('eye-login_senha');
    olho.src = '/static/img/default/open_eye.svg';

    formLogin.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'email': formLogin.email.value,
            'senha': formLogin.senha.value
        }

        let resp = await fetch(`${API_USUARIO_URL}/auth`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        let dadosLogin = await resp.json();

        if (resp.ok) {
            mostrarMensagem(dadosLogin.mensagem, dadosLogin.classe);

            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        }
        else {
            mostrarMensagem(dadosLogin.mensagem, dadosLogin.classe);
        }
    })
})