import { API_CATEGORIA_URL, mostrarMensagem, apiFetch, protegerRota } from "../main.js";

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota(['admin', 'superadmin']);
    if (!usuario) return;

    const formEditar = document.getElementById('form-editar');
    const voltar = document.getElementById('voltar');
    voltar.href = '/admin/gerenciar-categorias';

    let id = window.location.pathname.split("/").pop();

    let resp = await apiFetch(`${API_CATEGORIA_URL}/${id}`);
    let categoria = await resp.json();

    formEditar.nome.value = categoria.nome;
    formEditar.descricao.value = categoria.descricao;

    formEditar.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'nome': formEditar.nome.value,
            'descricao': formEditar.descricao.value
        }

        let resp = await apiFetch(`${API_CATEGORIA_URL}/${categoria.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        let dadosEditar = await resp.json();

        mostrarMensagem(dadosEditar.mensagem, dadosEditar.classe);
    })
})