import { API_USUARIO_URL, mostrarMensagem } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await carregarPerfil();

    let olho1 = document.getElementById('eye-perfil_senha');
    let olho2 = document.getElementById('eye-perfil_confirmar_senha');
    olho1.src = '/static/img/default/open_eye.svg';
    olho2.src = '/static/img/default/open_eye.svg';

    document.getElementById('foto-imagem').addEventListener('change', mostrarPreview);
    document.getElementById('form-editar-perfil').addEventListener('submit', editarPerfil);
});

async function carregarPerfil() {
    let resposta = await fetch(`${API_USUARIO_URL}/me`);
    let usuario = await resposta.json();

    document.getElementById('texto-email').textContent = usuario.email;
    document.getElementById('input-username').value = usuario.username;
    document.getElementById('preview-imagem').src = `/static/${usuario.url_foto}`;
}

function mostrarPreview(evento) {
    let arquivo = evento.target.files[0];
    if (!arquivo) return;

    let preview = document.getElementById('preview-imagem');
    preview.src = URL.createObjectURL(arquivo);
}

async function editarPerfil(evento) {
    evento.preventDefault();

    let form = document.getElementById('form-editar-perfil');
    let formData = new FormData(form);

    let resposta = await fetch(`${API_USUARIO_URL}/me`, {
        method: 'PUT',
        body: formData
    });

    let dados = await resposta.json();

    if (resposta.ok) {
        document.getElementById('perfil_senha').value = '';
        document.getElementById('perfil_confirmar_senha').value = '';

        setTimeout(() => {
            window.location.href = '/';
        }, 1500);
    }

    mostrarMensagem(dados.mensagem, dados.classe);
}