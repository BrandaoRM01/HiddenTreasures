import { API_DESTAQUE_URL, mostrarMensagem } from '../main.js';
import { listarDestaques } from './listar.js';

document.addEventListener('DOMContentLoaded', () => {
    const formDestaques = document.getElementById('form-destaques');

    formDestaques.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'nome': formDestaques.nome.value
        }

        let resp = await fetch(API_DESTAQUE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        let dadosCadastro = await resp.json();

        await listarDestaques();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);
    });
});