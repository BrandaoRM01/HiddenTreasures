import { API_PROMOCAO_URL, mostrarMensagem, apiFetch, protegerRota } from "../main.js";

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota(['admin', 'superadmin']);
    if (!usuario) return;

    const formEditar = document.getElementById('form-editar');
    const voltar = document.getElementById('voltar');
    voltar.href = '/admin/gerenciar-promocoes';

    let id = window.location.pathname.split("/").pop();

    let resp = await apiFetch(`${API_PROMOCAO_URL}/${id}`);
    let promocao = await resp.json();

    formEditar.titulo.value = promocao.titulo;
    formEditar.descricao.value = promocao.descricao;
    formEditar.desconto.value = promocao.desconto;
    formEditar.data_inicio.value = promocao.data_inicio;
    formEditar.data_fim.value = promocao.data_fim;

    formEditar.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'titulo': formEditar.titulo.value,
            'descricao': formEditar.descricao.value,
            'desconto': formEditar.desconto.value,
            'data_inicio': formEditar.data_inicio.value,
            'data_fim': formEditar.data_fim.value
        }

        let resp = await apiFetch(`${API_PROMOCAO_URL}/${promocao.id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        let dadosEditar = await resp.json();

        mostrarMensagem(dadosEditar.mensagem, dadosEditar.classe);
    })
})