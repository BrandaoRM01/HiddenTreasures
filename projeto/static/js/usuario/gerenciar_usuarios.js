import { API_USUARIO_URL, mostrarMensagem } from '../main.js';

let usuarioLogado = null;

document.addEventListener('DOMContentLoaded', async () => {
    await listarUsuarios();
});

export async function listarUsuarios() {
    let lista = document.getElementById('lista-usuarios');
    lista.innerHTML = '';

    let resposta = await fetch(`${API_USUARIO_URL}`);
    let dados = await resposta.json();

    usuarioLogado = dados.usuario_logado;

    dados.usuarios.forEach(usuario => {
        lista.appendChild(criarLinhaUsuario(usuario));
    });
}

function criarLinhaUsuario(usuario) {
    let atual = usuarioLogado;

    let linha = document.createElement('div');
    linha.className = 'd-flex justify-content-between align-items-center border-bottom py-2';
    linha.dataset.email = usuario.email;

    let infoWrapper = document.createElement('div');
    infoWrapper.className = 'd-flex align-items-center';

    let foto = document.createElement('img');
    foto.src = `/static/${usuario.url_foto}`;
    foto.width = 40;
    foto.height = 40;
    foto.style.objectFit = 'cover';
    foto.className = 'rounded-circle me-2';

    let textos = document.createElement('div');
    textos.innerHTML = `
        <strong>${usuario.username}</strong><br>
        <small>${usuario.email}</small><br>
        <span class="badge bg-secondary">${usuario.tipo_usuario}</span>
    `;

    infoWrapper.appendChild(foto);
    infoWrapper.appendChild(textos);
    linha.appendChild(infoWrapper);

    let podeGerenciar = atual.tipo_usuario === 'superadmin' && usuario.tipo_usuario !== 'superadmin';

    if (podeGerenciar) {
        let acoes = document.createElement('div');
        acoes.className = 'd-flex gap-2';

        let botaoPermissao = document.createElement('button');
        botaoPermissao.type = 'button';
        botaoPermissao.className = usuario.tipo_usuario === 'admin'
            ? 'btn btn-secondary btn-sm flex-fill'
            : 'btn btn-warning btn-sm flex-fill';
        botaoPermissao.textContent = usuario.tipo_usuario === 'admin' ? 'Remover Admin' : 'Tornar Admin';
        botaoPermissao.addEventListener('click', () => alterarPermissao(usuario, linha));

        let botaoExcluir = document.createElement('button');
        botaoExcluir.type = 'button';
        botaoExcluir.className = 'btn btn-danger flex-fill';
        botaoExcluir.title = 'Excluir';
        botaoExcluir.innerHTML = '<i class="bi bi-trash"></i>';
        botaoExcluir.addEventListener('click', () => excluirUsuario(usuario, linha));

        acoes.appendChild(botaoPermissao);
        acoes.appendChild(botaoExcluir);
        linha.appendChild(acoes);
    }

    return linha;
}

async function alterarPermissao(usuario, linha) {
    let novoTipo = usuario.tipo_usuario === 'admin' ? 'user' : 'admin';

    let formData = new FormData();
    formData.append('tipo_usuario', novoTipo);

    let resposta = await fetch(`${API_USUARIO_URL}/${usuario.email}`, {
        method: 'PUT',
        body: formData
    });

    let dados = await resposta.json();

    if (resposta.ok) {
        usuario.tipo_usuario = novoTipo;
        let novaLinha = criarLinhaUsuario(usuario);
        linha.replaceWith(novaLinha);
    }

    mostrarMensagem(dados.mensagem, dados.classe);
}

async function excluirUsuario(usuario, linha) {
    let confirmar = confirm(`Tem certeza que deseja excluir o usuário ${usuario.username}?`);
    if (!confirmar) return;

    let resposta = await fetch(`${API_USUARIO_URL}/${usuario.email}`, {
        method: 'DELETE'
    });

    let dados = await resposta.json();

    if (resposta.ok) {
        linha.remove();
    }

    mostrarMensagem(dados.mensagem, dados.classe);
}