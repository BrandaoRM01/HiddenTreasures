import { API_USUARIO_URL, mostrarMensagem, apiFetch } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    let formCadastro = document.getElementById('form-cadastro');

    let login = document.getElementById('login');
    login.href = '/login';

    let olho1 = document.getElementById('eye-senha');
    let olho2 = document.getElementById('eye-confirmar_senha');
    olho1.src = '/static/img/default/open_eye.svg';
    olho2.src = '/static/img/default/open_eye.svg';

    let previewImagem = document.getElementById('preview-imagem');
    previewImagem.src = '/static/img/default/user_foto.webp';

    formCadastro.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = new FormData(formCadastro);

        let resp = await apiFetch(API_USUARIO_URL, {
            method: 'POST',
            body: dados
        });

        let dadosCadastro = await resp.json();

        if (resp.ok) {
            sessionStorage.setItem('mensagemPendente', JSON.stringify({
                mensagem: dadosCadastro.mensagem,
                classe: dadosCadastro.classe
            }));

            window.location.href = '/login';
        }
        else {
            mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);
        }

    })
})