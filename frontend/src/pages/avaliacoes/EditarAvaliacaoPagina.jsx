import { useEffect, useState } from "react";
import { NavLink, useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import EstrelasNota from "../../components/EstrelasNota";
import "../pontos/detalhes.css";

function EditarAvaliacaoPagina() {
    const navigate = useNavigate();

    const { id } = useParams();

    const [pontoNome, setPontoNome] = useState(null);
    const [nota, setNota] = useState("");
    const [comentario, setComentario] = useState("");
    const [carregado, setCarregado] = useState(false);
    const [salvando, setSalvando] = useState(false);

    useEffect(() => {
        async function carregarAvaliacao() {
            try {
                const res = await api.get(`/api/avaliacoes/ponto/${id}`, {params: {status: "aprovado"}});

                if(!res.data.avaliacao_usuario) {
                    throw new Error("sem avaliação");
                }

                setPontoNome(res.data.ponto_nome);
                setNota(res.data.avaliacao_usuario.nota);
                setComentario(res.data.avaliacao_usuario.comentario || "");
                setCarregado(true);
            } catch (error) {
                mostrarMensagem("Avaliação não encontrada.", "danger");
                navigate(`/pontos/${id}`, {replace: true});
            }
        }

        carregarAvaliacao();
    }, [id])

    async function salvar(e) {
        e.preventDefault();

        if(!nota) {
            mostrarMensagem("Selecione uma nota antes de salvar.", "danger");
            return;
        }

        try {
            setSalvando(true);

            const res = await api.put(`/api/avaliacoes/ponto/${id}`, {nota, comentario});

            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        } finally {
            setSalvando(false);
        }
    }

    return (
        <>
            <div className="mt-4 pagina-avaliacoes">
                {carregado && (
                    <div className="card shadow-sm mb-4">
                        <div className="card-body">
                            <h4 className="mb-3">Editar Avaliação de <strong>{pontoNome}</strong></h4>

                            <form onSubmit={salvar}>
                                <div className="mb-3">
                                    <label className="form-label">Nota <span className="text-danger">*</span></label>
                                    <EstrelasNota valor={nota} onChange={setNota} />
                                </div>

                                <div className="mb-3">
                                    <label htmlFor="comentario" className="form-label">Comentário</label>
                                    <textarea id="comentario" className="form-control" rows="3"
                                        value={comentario} onChange={(e) => setComentario(e.target.value)}></textarea>
                                </div>

                                <button type="submit" className="btn btn-primary me-2" disabled={salvando}>
                                    {salvando ? "Salvando..." : "Salvar"}
                                </button>

                                <NavLink to={`/pontos/${id}`} className="btn btn-secondary">Voltar</NavLink>
                            </form>
                        </div>
                    </div>
                )}
            </div>
        </>
    )
}

export default EditarAvaliacaoPagina;
