import { API_CATEGORIA_URL, mostrarMensagem, apiFetch } from '../main.js';
import { listarCategorias } from './listar.js';

document.addEventListener('DOMContentLoaded', () => {
    const formCategoria = document.getElementById('form-categoria');

    formCategoria.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'nome': formCategoria.nome.value,
            'descricao': formCategoria.descricao.value
        }

        let resp = await apiFetch(API_CATEGORIA_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        let dadosCadastro = await resp.json();

        await listarCategorias();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);
    });
});