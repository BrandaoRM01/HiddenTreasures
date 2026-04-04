document.addEventListener("DOMContentLoaded", function () {

    const starsContainer = document.querySelector(".stars");
    const estrelas = starsContainer.querySelectorAll(".star");
    const notaInput = document.getElementById("nota");

    // Inicializa as estrelas conforme o valor atual
    const notaInicial = parseInt(notaInput.value);
    estrelas.forEach(s => {
        const value = parseInt(s.getAttribute("data-value"));
        if (value <= notaInicial) s.classList.add("active");
    });

    estrelas.forEach(star => {

        star.addEventListener("click", function () {
            const value = parseInt(this.getAttribute("data-value"));
            notaInput.value = value;

            // Atualiza cores
            estrelas.forEach(s => s.classList.remove("active"));
            estrelas.forEach(s => {
                if (parseInt(s.getAttribute("data-value")) <= value) s.classList.add("active");
            });
        });

        star.addEventListener("mouseover", function () {
            const value = parseInt(this.getAttribute("data-value"));

            estrelas.forEach(s => s.classList.remove("active"));
            estrelas.forEach(s => {
                if (parseInt(s.getAttribute("data-value")) <= value) s.classList.add("active");
            });
        });

        star.addEventListener("mouseout", function () {
            const currentValue = parseInt(notaInput.value);

            estrelas.forEach(s => s.classList.remove("active"));
            estrelas.forEach(s => {
                if (parseInt(s.getAttribute("data-value")) <= currentValue) s.classList.add("active");
            });
        });

    });

});