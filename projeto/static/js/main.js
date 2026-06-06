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

document.addEventListener("DOMContentLoaded", function () {

    let eyes = document.querySelectorAll(".toggle-password");

    eyes.forEach(el => {
        el.addEventListener("click", function () {

            let targetId = this.getAttribute("data-target");
            let input = document.getElementById(targetId);
            let icon = document.getElementById("eye-" + targetId);

            if (!input || !icon) return;

            if (input.type === "password") {
                input.type = "text";
                icon.src = "/static/img/default/close_eye.svg";
            } else {
                input.type = "password";
                icon.src = "/static/img/default/open_eye.svg";
            }
        });
    });

});

document.addEventListener('DOMContentLoaded', () => {
    let tipoPonto = document.getElementById('tipo_ponto');
    let camposNatural = document.getElementById('campos-natural');
    let camposCultural = document.getElementById('campos-cultural');

    if (!tipoPonto || !camposNatural || !camposCultural) {
        return;
    }

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
});