import { API_TIPO_CULTURAL_URL, mostrarMensagem, apiFetch } from '../main.js';
import { listarTiposCulturais } from './listar.js';

document.addEventListener('DOMContentLoaded', () => {
    const formTipoCultural = document.getElementById('form-tipo-cultural');

    formTipoCultural.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = {
            'nome': formTipoCultural.nome.value
        }

        let resp = await apiFetch(API_TIPO_CULTURAL_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });

        let dadosCadastro = await resp.json();

        await listarTiposCulturais();
        mostrarMensagem(dadosCadastro.mensagem, dadosCadastro.classe);
    });
});