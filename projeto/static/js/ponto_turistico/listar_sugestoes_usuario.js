import { API_PONTO_URL, API_CATEGORIA_URL, API_PROMOCAO_URL, API_ECOSSISTEMA_URL, API_TIPO_CULTURAL_URL, API_DESTAQUE_URL, mostrarMensagem } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    await carregarCategorias();
    await listarSugestoes();
    await carregarPromocoes();
    await carregarEcossistemas();
    await carregarTiposCulturais();
    await carregarDestaques();

    let inputFoto = document.getElementById('foto-imagem');
    let preview = document.getElementById('preview-imagem');

    inputFoto.addEventListener('change', () => {
        let arquivo = inputFoto.files[0];
        if (!arquivo) return;

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

export async function listarSugestoes() {
    let lista = document.getElementById('lista-sugestoes');
    lista.innerHTML = '';

    let resposta = await fetch(`${API_PONTO_URL}/minhas-sugestoes`);
    let dados = await resposta.json();

    if (dados.length == 0) {
        let div = document.createElement('div');
        div.className = 'text-center py-5';

        let icone = document.createElement('i');
        icone.className = 'bi bi-map display-1 text-secondary';

        let h3 = document.createElement('h3');
        h3.className = 'mt-3';
        h3.textContent = 'Nenhum ponto sugerido por você';

        let p = document.createElement('p');
        p.className = 'text-muted';
        p.textContent = 'Comece sugerindo um ponto turístico para a comunidade.';

        div.appendChild(icone);
        div.appendChild(h3);
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
        cartao.className = 'card border shadow-sm';

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

        textos.appendChild(nome);
        textos.appendChild(localizacao);
        textos.appendChild(categoria);
        textos.appendChild(tipo);

        if (ponto.promocao && ponto.promocao.titulo) {
            let promocao = document.createElement('p');
            promocao.className = 'mb-1';
            promocao.innerHTML = `<strong>Promoção:</strong> ${ponto.promocao.titulo}`;
            textos.appendChild(promocao);
        }

        if (ponto.media_avaliacao != null && ponto.media_avaliacao != undefined) {
            let avaliacao = document.createElement('p');
            avaliacao.className = 'mb-0 text-warning';
            avaliacao.textContent = `⭐ ${ponto.media_avaliacao.toFixed(1)}`;
            textos.appendChild(avaliacao);
        }

        grupoImagem.appendChild(imagem);
        grupoImagem.appendChild(textos);
        colunaInfo.appendChild(grupoImagem);

        let acoes = document.createElement('div');
        acoes.className = 'col-lg-4 text-lg-end mt-3 mt-lg-0';

        let statusEscrita = document.createElement('span');
        statusEscrita.className = 'badge fs-6 mb-3 ';

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

        if (ponto.status == 'pendente' || ponto.status == 'rejeitado') {
            let editar = document.createElement('a');
            editar.href = `/editar-sugestao/${ponto.id}`;
            editar.className = 'btn btn-warning';
            editar.innerHTML = '<i class="bi bi-pencil-fill"></i>';

            let excluir = document.createElement('button');
            excluir.type = 'button';
            excluir.className = 'btn btn-danger';
            excluir.innerHTML = '<i class="bi bi-trash-fill"></i>';
            removerSugestao(excluir, ponto, coluna);

            botoes.appendChild(editar);
            botoes.appendChild(excluir);
        } else {
            let bloqueado = document.createElement('button');
            bloqueado.type = 'button';
            bloqueado.className = 'btn btn-outline-secondary';
            bloqueado.disabled = true;
            bloqueado.innerHTML = '<i class="bi bi-lock-fill"></i> Sugestão Aprovada';
            botoes.appendChild(bloqueado);
        }

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

function removerSugestao(botao, ponto, coluna) {
    botao.addEventListener('click', async () => {
        let confirmar = confirm(`Tem certeza que deseja excluir a sugestão ${ponto.nome}?`);
        if (!confirmar) return;

        let resposta = await fetch(`${API_PONTO_URL}/${ponto.id}`, { method: 'DELETE' });
        let dados = await resposta.json();

        coluna.remove();
        mostrarMensagem(dados.mensagem, dados.classe);
    });
}

async function carregarCategorias() {
    let resposta = await fetch(API_CATEGORIA_URL);
    let categorias = await resposta.json();

    if (categorias.length == 0) {
        document.getElementById('aviso-sem-categoria').classList.remove('d-none');
        document.getElementById('card-form-sugestao').classList.add('d-none');
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
    if (promocoes.length == 0) return;

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
    if (destaques.length == 0) return;

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