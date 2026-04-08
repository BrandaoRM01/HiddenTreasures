let input_foto = document.getElementById('foto-imagem');
let preview_imagem = document.getElementById('preview-imagem');

preview_imagem.addEventListener('click', () => {
    input_foto.click();
});

input_foto.addEventListener('change', (event) => {
    let file = event.target.files[0];
    if (file) {
        preview_imagem.src = URL.createObjectURL(file);
    }
});