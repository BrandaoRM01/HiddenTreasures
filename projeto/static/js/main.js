export const API_CATEGORIA_URL = '/api/categorias';
export const API_ECOSSISTEMA_URL = '/api/ecossistemas';
export const API_DESTAQUE_URL = '/api/destaques';
export const API_TIPO_CULTURAL_URL = '/api/tipos_culturais';
export const API_PROMOCAO_URL = '/api/promocoes';
export const API_PONTO_URL = '/api/pontos';
export const API_USUARIO_URL = '/api/usuarios';
export const API_AVALIACAO_URL = '/api/avaliacoes';

let input_foto = document.getElementById('foto-imagem');
let preview_imagem = document.getElementById('preview-imagem');

if (input_foto && preview_imagem) {

    preview_imagem.addEventListener('click', () => {
        input_foto.click();
    });

    input_foto.addEventListener('change', (event) => {
        let file = event.target.files[0];

        if (file) {
            preview_imagem.src = URL.createObjectURL(file);
        }
    });

}

document.addEventListener('DOMContentLoaded', () => {

    let eyes = document.querySelectorAll('.toggle-password');

    eyes.forEach(el => {

        el.addEventListener('click', function () {

            let targetId = this.getAttribute('data-target');
            let input = document.getElementById(targetId);
            let icon = document.getElementById('eye-' + targetId);

            if (!input || !icon) {
                return;
            }

            if (input.type === 'password') {
                input.type = 'text';
                icon.src = '/static/img/default/close_eye.svg';
            } else {
                input.type = 'password';
                icon.src = '/static/img/default/open_eye.svg';
            }

        });

    });

    let tipoPonto = document.getElementById('tipo_ponto');
    let camposNatural = document.getElementById('campos-natural');
    let camposCultural = document.getElementById('campos-cultural');

    if (tipoPonto && camposNatural && camposCultural) {

        function atualizarCamposPonto() {

            if (tipoPonto.value === 'natural') {
                camposNatural.classList.remove('d-none');
                camposCultural.classList.add('d-none');
            } else {
                camposNatural.classList.add('d-none');
                camposCultural.classList.remove('d-none');
            }

        }

        tipoPonto.addEventListener('change', atualizarCamposPonto);

        atualizarCamposPonto();

    }

    let checks = document.querySelectorAll('.destaque-checkbox');

    checks.forEach(check => {

        check.addEventListener('change', () => {

            let selecionados = document.querySelectorAll('.destaque-checkbox:checked');

            if (selecionados.length > 3) {
                check.checked = false;
                alert('Você pode selecionar no máximo 3 destaques.');
            }

        });

    });

});

export function mostrarMensagem(mensagem, tipo = "success") {

    const container = document.getElementById("container-alertas");

    const alerta = document.createElement("div");
    alerta.className = `alerta-toast alerta-${tipo}`;

    let icone = "";

    if (tipo === "success") {
        icone = "bi bi-check-circle-fill";
    } else if (tipo === "danger") {
        icone = "bi bi-x-circle-fill";
    } else if (tipo === "warning") {
        icone = "bi bi-exclamation-triangle-fill";
    } else if (tipo === "info") {
        icone = "bi bi-info-circle-fill";
    }

    alerta.innerHTML = `
        <i class="${icone} icone"></i>
        <span class="mensagem">${mensagem}</span>
        <button class="fechar">&times;</button>
    `;

    container.appendChild(alerta);

    const fechar = alerta.querySelector(".fechar");

    fechar.addEventListener("click", () => {
        removerAlerta(alerta);
    });

    setTimeout(() => {
        removerAlerta(alerta);
    }, 4000);
}

function removerAlerta(alerta) {

    alerta.style.animation = "desaparecerToast 0.3s ease";

    setTimeout(() => {
        alerta.remove();
    }, 300);
}

export function criarFaixaDestaques(destaques) {
    let faixa = document.createElement('div');
    faixa.className = 'position-absolute bottom-0 start-0 w-100 p-2 d-flex flex-wrap gap-1';
    faixa.style.background = 'linear-gradient(to top, rgba(0,0,0,0.6), transparent)';

    destaques.forEach(destaque => {
        let badge = document.createElement('span');
        badge.className = 'badge bg-dark bg-opacity-75 text-white';
        badge.textContent = `#${destaque.nome}`;
        faixa.appendChild(badge);
    });

    return faixa;
}

export function criarAvaliacao(ponto) {
    let avaliacao = document.createElement('p');
    avaliacao.className = 'text-warning';

    let media = ponto.media_avaliacao !== null && ponto.media_avaliacao !== undefined ? Number(ponto.media_avaliacao) : null;

    if (media !== null) {
        avaliacao.textContent = `⭐ ${media.toFixed(1)}`;
    } else {
        avaliacao.textContent = '⭐ Nenhuma avaliação';
    }

    return avaliacao;
}

export function criarPreco(ponto) {
    let preco = document.createElement('p');
    preco.className = 'preco mb-0';

    let custoEntrada = Number(ponto.custo_entrada);

    if (custoEntrada) {
        if (ponto.promocao) {
            let precoAntigo = document.createElement('span');
            precoAntigo.className = 'preco-antigo';
            precoAntigo.textContent = `R$ ${custoEntrada.toFixed(2)}`;

            let valorComDesconto = custoEntrada * (1 - Number(ponto.promocao.desconto) / 100);

            let precoPromocao = document.createElement('span');
            precoPromocao.className = 'preco-promocao';
            precoPromocao.textContent = `R$ ${valorComDesconto.toFixed(2)}`;

            preco.appendChild(precoAntigo);
            preco.appendChild(precoPromocao);
        } else {
            preco.textContent = `R$ ${custoEntrada.toFixed(2)}`;
        }
    } else {
        let precoGratuito = document.createElement('span');
        precoGratuito.className = 'preco-promocao';
        precoGratuito.textContent = 'Gratuito';
        preco.appendChild(precoGratuito);
    }

    return preco;
}

export function criarBotaoDetalhes(ponto) {
    let botao = document.createElement('a');
    botao.href = `/detalhes-ponto/${ponto.id}`;
    botao.className = 'btn btn-primary w-100 mt-2';
    botao.textContent = 'Ver detalhes';
    return botao;
}

export function atualizarCoracao(coracao, favorito) {
    if (favorito) {
        coracao.style.color = 'red';
        coracao.textContent = '❤️';
    } else {
        coracao.style.color = 'gray';
        coracao.textContent = '🤍';
    }
}

export function criarBotaoFavorito(ponto, aoAlternar) {
    let botao = document.createElement('button');
    botao.type = 'button';
    botao.className = 'btn btn-light rounded-circle shadow-sm d-flex align-items-center justify-content-center';
    botao.style.width = '40px';
    botao.style.height = '40px';

    let coracao = document.createElement('span');
    coracao.style.fontSize = '20px';
    atualizarCoracao(coracao, ponto.favorito);

    botao.appendChild(coracao);

    botao.addEventListener('click', async () => {
        let resposta = await fetch(`${API_USUARIO_URL}/favoritos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ponto_id: ponto.id })
        });

        let dadosResposta = await resposta.json();

        if (resposta.ok) {
            ponto.favorito = dadosResposta.favorito;
            atualizarCoracao(coracao, ponto.favorito);

            if (aoAlternar) {
                aoAlternar(ponto.favorito);
            }
        }

        mostrarMensagem(dadosResposta.mensagem, dadosResposta.classe);
    });

    return botao;
}
export function inicializarEstrelas() {
    let estrelas = document.querySelectorAll('.star');
    let notaInput = document.getElementById('nota');

    if (!estrelas.length || !notaInput) return;

    function marcarEstrelas(valor) {
        estrelas.forEach(s => {
            s.classList.toggle('active', s.getAttribute('data-value') <= valor);
        });
    }

    estrelas.forEach(star => {
        star.addEventListener('click', function () {
            notaInput.value = this.getAttribute('data-value');
            marcarEstrelas(notaInput.value);
        });

        star.addEventListener('mouseover', function () {
            marcarEstrelas(this.getAttribute('data-value'));
        });

        star.addEventListener('mouseout', function () {
            marcarEstrelas(notaInput.value);
        });
    });
}