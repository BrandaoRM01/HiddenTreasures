import { api, mensagemDeErro } from "./api";
import { mostrarMensagem } from "./mensagem";

export async function alterarStatusAvaliacao(idPonto, avaliacao, status) {
    try {
        const res = await api.put(`/api/avaliacoes/ponto/${idPonto}`,
            { nota: avaliacao.nota, comentario: avaliacao.comentario, status },
            { params: { usuario_email: avaliacao.usuario.email } });

        mostrarMensagem(res.data.mensagem, res.data.classe);
        return true;
    } catch (error) {
        mostrarMensagem(mensagemDeErro(error), "danger");
        return false;
    }
}

export async function excluirAvaliacao(idPonto, usuarioEmail, username) {
    const mensagem = username
        ? `Tem certeza que deseja excluir a avaliação de ${username}?`
        : "Tem certeza que deseja excluir sua avaliação?";

    if (!window.confirm(mensagem)) {
        return false;
    }

    try {
        const res = await api.delete(`/api/avaliacoes/ponto/${idPonto}`, { params: { usuario_email: usuarioEmail } });

        mostrarMensagem(res.data.mensagem, res.data.classe);
        return true;
    } catch (error) {
        mostrarMensagem(mensagemDeErro(error), "danger");
        return false;
    }
}
