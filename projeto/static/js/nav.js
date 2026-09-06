import { API_USUARIO_URL, apiFetch, mostrarMensagem } from './main.js';

document.addEventListener('DOMContentLoaded', async () => {
    exibirMensagemPendente();

    await montarNavbar();

    configurarLinksDeNavegacao();

    document.getElementById('btn-logout').addEventListener('click', fazerLogout);
    document.getElementById('btn-excluir-perfil').addEventListener('click', excluirPerfil);
});

function configurarLinksDeNavegacao() {
    const links = {
        'link-home-brand': '/',
        'link-home': '/',
        'link-pontos': '/pontos',
        'link-sugerir-ponto': '/sugerir-ponto',
        'link-favoritos': '/favoritos',
        'link-sobre': '/sobre',
        'link-painel-admin': '/admin/painel-admin',
        'link-login': '/login',
        'link-cadastro': '/cadastro',
        'link-editar-perfil': '/editar-perfil'
    };

    for (let id in links) {
        document.getElementById(id).addEventListener('click', (evento) => {
            evento.preventDefault();
            window.location.href = links[id];
        });
    }
}

function exibirMensagemPendente() {
    let pendente = sessionStorage.getItem('mensagemPendente');

    if (!pendente) return;

    sessionStorage.removeItem('mensagemPendente');

    let { mensagem, classe } = JSON.parse(pendente);
    mostrarMensagem(mensagem, classe);
}

async function montarNavbar() {
    let token = localStorage.getItem('token');

    if (!token) {
        mostrarComoVisitante();
        return;
    }

    let resposta = await apiFetch(`${API_USUARIO_URL}/me`);

    if (!resposta.ok) {
        localStorage.removeItem('token');
        mostrarComoVisitante();
        return;
    }

    let usuario = await resposta.json();
    mostrarComoLogado(usuario);
}

function mostrarComoVisitante() {
    document.getElementById('area-auth').classList.remove('d-none');
    document.getElementById('area-usuario').classList.add('d-none');
    document.getElementById('item-sugerir-ponto').classList.add('d-none');
    document.getElementById('item-favoritos').classList.add('d-none');
    document.getElementById('item-painel-admin').classList.add('d-none');
}

function mostrarComoLogado(usuario) {
    let ehModerador = usuario.tipo_usuario == 'admin' || usuario.tipo_usuario == 'superadmin';

    document.getElementById('area-auth').classList.add('d-none');
    document.getElementById('area-usuario').classList.remove('d-none');

    document.getElementById('item-sugerir-ponto').classList.toggle('d-none', ehModerador);
    document.getElementById('item-favoritos').classList.remove('d-none');
    document.getElementById('item-painel-admin').classList.toggle('d-none', !ehModerador);
    document.getElementById('item-excluir-perfil').classList.toggle('d-none', usuario.tipo_usuario == 'superadmin');

    document.getElementById('navbar-foto-usuario').src = `/static/${usuario.url_foto}`;
    document.getElementById('navbar-username').textContent = usuario.username;
}

async function fazerLogout(evento) {
    evento.preventDefault();

    let resposta = await apiFetch('/logout', { method: 'POST' });
    let dados = await resposta.json();

    localStorage.removeItem('token');

    sessionStorage.setItem('mensagemPendente', JSON.stringify({
        mensagem: dados.mensagem,
        classe: dados.classe
    }));

    window.location.href = '/';
}

async function excluirPerfil(evento) {
    evento.preventDefault();

    let confirmar = confirm('Tem certeza que deseja excluir seu perfil?');
    if (!confirmar) return;

    let resposta = await apiFetch(`${API_USUARIO_URL}/me`, {
        method: 'DELETE'
    });

    let dados = await resposta.json();

    if (resposta.ok) {
        localStorage.removeItem('token');

        sessionStorage.setItem('mensagemPendente', JSON.stringify({
            mensagem: dados.mensagem,
            classe: dados.classe
        }));

        window.location.href = '/';
    } else {
        mostrarMensagem(dados.mensagem, dados.classe);
    }
}