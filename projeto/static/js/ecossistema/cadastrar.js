import { API_ECOSSISTEMA_URL, mostrarMensagem } from '../main.js';
import { listarEcossistemas } from './listar.js';

document.addEventListener('DOMContentLoaded', () => {
    const formEcossistemas = document.getElementById('form-ecossistemas');

    formEcossistemas.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'nome': formEcossistemas.nome.value
        }

        let resp = await fetch(API_ECOSSISTEMA_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        let dadosCadastro = await resp.json();

        await listarEcossistemas();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);
    });
});