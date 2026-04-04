document.addEventListener("DOMContentLoaded", function () {

    let estrelas = document.querySelectorAll(".star");
    let nota_input = document.getElementById("nota");

    estrelas.forEach(star => {
        star.addEventListener("click", function () {
            let value = this.getAttribute("data-value");

            nota_input.value = value;

            estrelas.forEach(s => s.classList.remove("active"));

            estrelas.forEach(s => {
                if (s.getAttribute("data-value") <= value) {
                    s.classList.add("active");
                }
            });
        });

        star.addEventListener("mouseover", function () {
            let value = this.getAttribute("data-value");

            estrelas.forEach(s => s.classList.remove("active"));

            estrelas.forEach(s => {
                if (s.getAttribute("data-value") <= value) {
                    s.classList.add("active");
                }
            });
        });

        star.addEventListener("mouseout", function () {
            let selected = nota_input.value;

            estrelas.forEach(s => s.classList.remove("active"));

            estrelas.forEach(s => {
                if (s.getAttribute("data-value") <= selected) {
                    s.classList.add("active");
                }
            });
        });
    });

});