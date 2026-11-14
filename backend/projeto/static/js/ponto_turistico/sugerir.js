import { API_PONTO_URL, mostrarMensagem, apiFetch, protegerRota } from '../main.js';
import { listarSugestoes } from './listar_sugestoes_usuario.js';

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota('user');
    if (!usuario) return;

    let form = document.getElementById('form-sugestao');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = new FormData(form);

        let resposta = await apiFetch(API_PONTO_URL, {
            method: 'POST',
            body: dados
        });

        let dadosCadastro = await resposta.json();

        await listarSugestoes();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);

        if (resposta.ok) {
            form.reset();
            document.getElementById('preview-imagem').src = '/static/img/default/hidden_treasures_logo.png';
        }
    });
});