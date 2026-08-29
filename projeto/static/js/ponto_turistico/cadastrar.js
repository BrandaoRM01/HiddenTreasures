import { API_PONTO_URL, mostrarMensagem } from '../main.js';
import { listarPontos } from './listar.js';

document.addEventListener('DOMContentLoaded', () => {
    let form = document.getElementById('form-pontos');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = new FormData(form);

        let resposta = await fetch(API_PONTO_URL, {
            method: 'POST',
            body: dados
        });

        let dadosCadastro = await resposta.json();

        await listarPontos();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);

        if (resposta.ok) {
            form.reset();
            document.getElementById('preview-imagem').src = '/static/img/default/hidden_treasures_logo.png';
        }
    });
});