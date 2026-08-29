import { API_PROMOCAO_URL, mostrarMensagem } from '../main.js';
import { listarPromocoes } from './listar.js';

document.addEventListener('DOMContentLoaded', () => {
    const formPromocoes = document.getElementById('form-promocoes');

    formPromocoes.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'titulo': formPromocoes.titulo.value,
            'descricao': formPromocoes.descricao.value,
            'desconto': formPromocoes.desconto.value,
            'data_inicio': formPromocoes.data_inicio.value,
            'data_fim': formPromocoes.data_fim.value
        }

        let resp = await fetch(API_PROMOCAO_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        let dadosCadastro = await resp.json();

        await listarPromocoes();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);
    });
});