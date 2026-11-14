import { API_TIPO_CULTURAL_URL, mostrarMensagem, apiFetch, protegerRota } from "../main.js";

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota(['admin', 'superadmin']);
    if (!usuario) return;

    const formEditar = document.getElementById('form-editar');
    const voltar = document.getElementById('voltar');
    voltar.href = '/admin/gerenciar-tipos-culturais';

    let id = window.location.pathname.split("/").pop();

    let resp = await apiFetch(`${API_TIPO_CULTURAL_URL}/${id}`);
    let tipo_cultural = await resp.json();

    formEditar.nome.value = tipo_cultural.nome;

    formEditar.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'nome': formEditar.nome.value
        }

        let resp = await apiFetch(`${API_TIPO_CULTURAL_URL}/${tipo_cultural.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        let dadosEditar = await resp.json();

        mostrarMensagem(dadosEditar.mensagem, dadosEditar.classe);
    })
})