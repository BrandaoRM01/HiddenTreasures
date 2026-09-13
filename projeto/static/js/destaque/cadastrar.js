import { API_DESTAQUE_URL, mostrarMensagem, apiFetch, protegerRota } from '../main.js';
import { listarDestaques } from './listar.js';

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota(['admin', 'superadmin']);
    if (!usuario) return;

    const formDestaques = document.getElementById('form-destaques');

    formDestaques.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'nome': formDestaques.nome.value
        }

        let resp = await apiFetch(API_DESTAQUE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        let dadosCadastro = await resp.json();

        await listarDestaques();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);
    });
});