export function mostrarMensagem(mensagem, classe = "success") {
    window.dispatchEvent(new CustomEvent("mensagem-flash", { detail: { mensagem, classe } }));
}
