import { API_PONTO_URL, API_CATEGORIA_URL, API_PROMOCAO_URL, API_ECOSSISTEMA_URL, API_TIPO_CULTURAL_URL, API_DESTAQUE_URL, mostrarMensagem, apiFetch, protegerRota } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota('user');
    if (!usuario) return;

    let voltar = document.getElementById('voltar');
    voltar.href = '/sugerir-ponto';
    let id = window.location.pathname.split('/').pop();

    let resposta = await apiFetch(`${API_PONTO_URL}/${id}`);
    let ponto = await resposta.json();

    let form = document.getElementById('form-editar');

    form.nome.value = ponto.nome;
    form.localizacao.value = ponto.localizacao;
    form.descricao.value = ponto.descricao;
    form.horario_funcionamento.value = ponto.horario_funcionamento;
    form.custo_entrada.value = ponto.custo_entrada;
    form.area_km.value = ponto.area_km || '';
    form.ano_fundacao.value = ponto.ano_fundacao || '';

    if (ponto.url_imagem) {
        document.getElementById('preview-imagem').src = `/static/${ponto.url_imagem}`;
    } else {
        document.getElementById('preview-imagem').src = '/static/img/default/hidden_treasures_logo.png';
    }

    let selectTipo = document.getElementById('tipo_ponto');
    let camposNatural = document.getElementById('campos-natural');
    let camposCultural = document.getElementById('campos-cultural');

    selectTipo.value = ponto.tipo_ponto;

    if (ponto.tipo_ponto == 'natural') {
        camposNatural.classList.remove('d-none');
        camposCultural.classList.add('d-none');
    } else {
        camposCultural.classList.remove('d-none');
        camposNatural.classList.add('d-none');
    }

    selectTipo.addEventListener('change', () => {
        let ehNatural = selectTipo.value == 'natural';
        camposNatural.classList.toggle('d-none', !ehNatural);
        camposCultural.classList.toggle('d-none', ehNatural);
    });

    let respostaCategorias = await apiFetch(API_CATEGORIA_URL);
    let selectCategoria = document.getElementById('categoria');
    let categorias = await respostaCategorias.json();

    categorias.forEach(categoria => {
        let option = document.createElement('option');
        option.textContent = categoria.nome;
        option.value = categoria.id;

        if (categoria.id == ponto.categoria.id) {
            option.selected = true;
        }

        selectCategoria.appendChild(option);
    });

    let respostaPromocoes = await apiFetch(`${API_PROMOCAO_URL}/ativas`);
    let selectPromocao = document.getElementById('promocao');
    let promocoes = await respostaPromocoes.json();

    promocoes.forEach(promocao => {
        let option = document.createElement('option');
        option.textContent = promocao.titulo;
        option.value = promocao.id;

        if (ponto.promocao && promocao.id == ponto.promocao.id) {
            option.selected = true;
        }

        selectPromocao.appendChild(option);
    });

    let respostaEcossistemas = await apiFetch(API_ECOSSISTEMA_URL);
    let selectEcossistema = document.getElementById('ecossistema');
    let ecossistemas = await respostaEcossistemas.json();

    ecossistemas.forEach(ecossistema => {
        let option = document.createElement('option');
        option.textContent = ecossistema.nome;
        option.value = ecossistema.id;

        if (ponto.ecossistema && ecossistema.id == ponto.ecossistema.id) {
            option.selected = true;
        }

        selectEcossistema.appendChild(option);
    });

    let respostaTiposCulturais = await apiFetch(API_TIPO_CULTURAL_URL);
    let selectTipoCultural = document.getElementById('tipo_cultural');
    let tiposCulturais = await respostaTiposCulturais.json();

    tiposCulturais.forEach(tipo => {
        let option = document.createElement('option');
        option.textContent = tipo.nome;
        option.value = tipo.id;

        if (ponto.tipo_cultural && tipo.id == ponto.tipo_cultural.id) {
            option.selected = true;
        }

        selectTipoCultural.appendChild(option);
    });

    let respostaDestaques = await apiFetch(API_DESTAQUE_URL);
    let listaDestaques = document.getElementById('lista-destaques');
    let destaques = await respostaDestaques.json();

    let idsDestaquesPonto = ponto.destaques.map(destaque => destaque.id);

    destaques.forEach(destaque => {
        let input = document.createElement('input');
        input.type = 'checkbox';
        input.className = 'btn-check destaque-checkbox';
        input.id = `destaque${destaque.id}`;
        input.name = 'destaques';
        input.value = destaque.id;
        input.autocomplete = 'off';

        if (idsDestaquesPonto.includes(destaque.id)) {
            input.checked = true;
        }

        let label = document.createElement('label');
        label.className = 'btn btn-outline-primary destaque-chip';
        label.htmlFor = `destaque${destaque.id}`;
        label.textContent = destaque.nome;

        listaDestaques.appendChild(input);
        listaDestaques.appendChild(label);
    });

    document.querySelectorAll('.destaque-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            let selecionados = document.querySelectorAll('.destaque-checkbox:checked');

            if (selecionados.length > 3) {
                checkbox.checked = false;
                mostrarMensagem('Você pode selecionar no máximo 3 destaques.', 'danger');
            }
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        let dados = new FormData(form);

        let respostaEditar = await apiFetch(`${API_PONTO_URL}/${ponto.id}`, {
            method: 'PUT',
            body: dados
        });

        let dadosEditar = await respostaEditar.json();

        mostrarMensagem(dadosEditar.mensagem, dadosEditar.classe);
    });
});