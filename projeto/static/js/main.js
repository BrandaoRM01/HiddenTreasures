export const API_CATEGORIA_URL = '/api/categorias';
export const API_ECOSSISTEMA_URL = '/api/ecossistemas';
export const API_DESTAQUE_URL = '/api/destaques';
export const API_TIPO_CULTURAL_URL = '/api/tipos_culturais';
export const API_PROMOCAO_URL = '/api/promocoes';
export const API_PONTO_URL = '/api/pontos';
export const API_USUARIO_URL = '/api/usuarios';

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