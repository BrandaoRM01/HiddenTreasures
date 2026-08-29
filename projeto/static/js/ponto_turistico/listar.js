import { API_PONTO_URL, API_CATEGORIA_URL, API_PROMOCAO_URL, API_ECOSSISTEMA_URL, API_TIPO_CULTURAL_URL, API_DESTAQUE_URL, mostrarMensagem } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await listarPontos();
    await carregarCategorias();
    await carregarPromocoes();
    await carregarEcossistemas();
    await carregarTiposCulturais();
    await carregarDestaques();

    let inputFoto = document.getElementById('foto-imagem');
    let preview = document.getElementById('preview-imagem');

    inputFoto.addEventListener('change', () => {
        let arquivo = inputFoto.files[0];

        if (!arquivo) {
            return;
        }

        let leitor = new FileReader();
        leitor.onload = () => preview.src = leitor.result;
        leitor.readAsDataURL(arquivo);
    });

    let selectTipo = document.getElementById('tipo_ponto');
    let camposNatural = document.getElementById('campos-natural');
    let camposCultural = document.getElementById('campos-cultural');

    selectTipo.addEventListener('change', () => {
        let ehNatural = selectTipo.value == 'natural';
        camposNatural.classList.toggle('d-none', !ehNatural);
        camposCultural.classList.toggle('d-none', ehNatural);
    });

});

export async function listarPontos() {
    let lista = document.getElementById('lista-pontos');
    lista.innerHTML = '';

    document.getElementById('preview-imagem').src = '/static/img/default/hidden_treasures_logo.png';

    let resposta = await fetch(API_PONTO_URL);
    let dados = await resposta.json();

    if (dados.length == 0) {

        let div = document.createElement('div');
        div.className = 'text-center py-5';

        let icone = document.createElement('i');
        icone.className = 'bi bi-geo-alt display-1 text-secondary';

        let h4 = document.createElement('h4');
        h4.className = 'mb-2 mt-3';
        h4.textContent = 'Nenhum ponto cadastrado';

        let p = document.createElement('p');
        p.className = 'text-muted';
        p.textContent = 'Comece cadastrando um ponto turístico para aparecer aqui.';

        div.appendChild(icone);
        div.appendChild(h4);
        div.appendChild(p);

        lista.appendChild(div);

        return;
    }

    let linha = document.createElement('div');
    linha.className = 'row g-3';

    dados.forEach(ponto => {

        let coluna = document.createElement('div');
        coluna.className = 'col-12';

        let cartao = document.createElement('div');
        cartao.className = 'card shadow-sm border-0';

        let corpoCartao = document.createElement('div');
        corpoCartao.className = 'card-body';

        let linhaInterna = document.createElement('div');
        linhaInterna.className = 'row align-items-center';

        let colunaInfo = document.createElement('div');
        colunaInfo.className = 'col-lg-8';

        let grupoImagem = document.createElement('div');
        grupoImagem.className = 'd-flex align-items-center gap-3';

        let imagem = document.createElement('img');
        imagem.src = `/static/${ponto.url_imagem}`;
        imagem.alt = ponto.nome;
        imagem.className = 'rounded shadow-sm';
        imagem.style.width = '100px';
        imagem.style.height = '100px';
        imagem.style.objectFit = 'cover';

        let textos = document.createElement('div');

        let nome = document.createElement('h5');
        nome.className = 'fw-bold mb-1';
        nome.textContent = ponto.nome;

        let localizacao = document.createElement('p');
        localizacao.className = 'text-muted mb-1';
        localizacao.innerHTML = `<i class="bi bi-geo-alt-fill"></i> ${ponto.localizacao}`;

        let categoria = document.createElement('p');
        categoria.className = 'mb-1';
        categoria.innerHTML = `<strong>Categoria:</strong> ${ponto.categoria.nome}`;

        let tipo = document.createElement('p');
        tipo.className = 'mb-1';
        let tipoLabel = ponto.tipo_ponto.charAt(0).toUpperCase() + ponto.tipo_ponto.slice(1);
        tipo.innerHTML = `<strong>Tipo:</strong> ${tipoLabel}`;

        let promocao = document.createElement('p');
        if (ponto.promocao && ponto.promocao.titulo) {
            promocao.className = 'mb-1';
            promocao.innerHTML = `<strong>Promoção:</strong> ${ponto.promocao.titulo}`;
        } else {
            promocao.className = 'mb-1 text-muted';
            promocao.textContent = 'Nenhuma promoção ativa';
        }

        let avaliacao = document.createElement('span');
        if (ponto.media_avaliacao !== null && ponto.media_avaliacao !== undefined) {
            avaliacao.className = 'badge text-warning';
            avaliacao.textContent = `⭐ ${ponto.media_avaliacao.toFixed(1)}`;
        } else {
            avaliacao.className = 'badge bg-secondary';
            avaliacao.textContent = 'Sem avaliações';
        }

        textos.appendChild(nome);
        textos.appendChild(localizacao);
        textos.appendChild(categoria);
        textos.appendChild(tipo);
        textos.appendChild(promocao);
        textos.appendChild(avaliacao);

        grupoImagem.appendChild(imagem);
        grupoImagem.appendChild(textos);
        colunaInfo.appendChild(grupoImagem);

        let acoes = document.createElement('div');
        acoes.className = 'col-lg-4 text-lg-end mt-3 mt-lg-0';

        let statusEscrita = document.createElement('span');
        statusEscrita.className = 'fs-6 mb-3 badge ';

        if (ponto.status == 'aprovado') {
            statusEscrita.className += 'bg-success';
            statusEscrita.innerHTML = '<i class="bi bi-check-circle-fill"></i> Aprovado';
        } else if (ponto.status == 'rejeitado') {
            statusEscrita.className += 'bg-danger';
            statusEscrita.innerHTML = '<i class="bi bi-x-circle-fill"></i> Rejeitado';
        } else {
            statusEscrita.className += 'bg-warning text-dark';
            statusEscrita.innerHTML = '<i class="bi bi-clock-fill"></i> Pendente';
        }

        let botoes = document.createElement('div');
        botoes.className = 'd-flex flex-wrap justify-content-lg-end gap-2';

        if (ponto.status == 'aprovado') {
            let editar = document.createElement('a');
            editar.href = `/admin/editar-ponto/${ponto.id}`;
            editar.className = 'btn btn-warning';
            editar.innerHTML = '<i class="bi bi-pencil-fill"></i>';
            botoes.appendChild(editar);
        }

        let excluir = document.createElement('button');
        excluir.type = 'button';
        excluir.className = 'btn btn-danger';
        excluir.innerHTML = '<i class="bi bi-trash-fill"></i>';

        removerPonto(excluir, ponto, coluna);

        botoes.appendChild(excluir);

        acoes.appendChild(statusEscrita);
        acoes.appendChild(document.createElement('br'));
        acoes.appendChild(botoes);

        linhaInterna.appendChild(colunaInfo);
        linhaInterna.appendChild(acoes);
        corpoCartao.appendChild(linhaInterna);
        cartao.appendChild(corpoCartao);
        coluna.appendChild(cartao);
        linha.appendChild(coluna);
    });

    lista.appendChild(linha);
}

function removerPonto(botao, ponto, coluna) {
    botao.addEventListener('click', async () => {

        let confirmar = confirm(`Tem certeza que deseja excluir o ponto turístico ${ponto.nome}?`);

        if (!confirmar) {
            return;
        }

        let respostaExcluir = await fetch(`${API_PONTO_URL}/${ponto.id}`, {
            method: 'DELETE'
        });

        let dadosExcluir = await respostaExcluir.json();

        coluna.remove();

        mostrarMensagem(dadosExcluir.mensagem, dadosExcluir.classe);
    });
}

async function carregarCategorias() {
    let resposta = await fetch(API_CATEGORIA_URL);
    let categorias = await resposta.json();

    if (categorias.length == 0) {
        document.getElementById('aviso-sem-categoria').classList.remove('d-none');
        document.getElementById('cadastrar-categoria').href = '/admin/gerenciar-categorias';
        return;
    }

    let select = document.getElementById('categoria');

    categorias.forEach(categoria => {
        let option = document.createElement('option');
        option.value = categoria.id;
        option.textContent = categoria.nome;
        select.appendChild(option);
    });
}

async function carregarPromocoes() {
    let resposta = await fetch(`${API_PROMOCAO_URL}/ativas`);
    let promocoes = await resposta.json();

    if (promocoes.length == 0) {
        return;
    }

    document.getElementById('campo-promocao').classList.remove('d-none');

    let select = document.getElementById('promocao');

    promocoes.forEach(promocao => {
        let option = document.createElement('option');
        option.value = promocao.id;
        option.textContent = promocao.titulo;
        select.appendChild(option);
    });
}

async function carregarEcossistemas() {
    let resposta = await fetch(API_ECOSSISTEMA_URL);
    let ecossistemas = await resposta.json();

    let select = document.getElementById('ecossistema');

    ecossistemas.forEach(ecossistema => {
        let option = document.createElement('option');
        option.value = ecossistema.id;
        option.textContent = ecossistema.nome;
        select.appendChild(option);
    });
}

async function carregarTiposCulturais() {
    let resposta = await fetch(API_TIPO_CULTURAL_URL);
    let tiposCulturais = await resposta.json();

    let select = document.getElementById('tipo_cultural');

    tiposCulturais.forEach(tipo => {
        let option = document.createElement('option');
        option.value = tipo.id;
        option.textContent = tipo.nome;
        select.appendChild(option);
    });
}

async function carregarDestaques() {
    let resposta = await fetch(API_DESTAQUE_URL);
    let destaques = await resposta.json();

    if (destaques.length == 0) {
        return;
    }

    document.getElementById('campo-destaques').classList.remove('d-none');

    let lista = document.getElementById('lista-destaques');

    destaques.forEach(destaque => {
        let input = document.createElement('input');
        input.type = 'checkbox';
        input.className = 'btn-check destaque-checkbox';
        input.id = `destaque${destaque.id}`;
        input.name = 'destaques';
        input.value = destaque.id;
        input.autocomplete = 'off';

        let label = document.createElement('label');
        label.className = 'btn btn-outline-primary destaque-chip';
        label.htmlFor = `destaque${destaque.id}`;
        label.textContent = destaque.nome;

        lista.appendChild(input);
        lista.appendChild(label);
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
}