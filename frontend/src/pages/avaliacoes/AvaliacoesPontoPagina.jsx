import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import { alterarStatusAvaliacao, excluirAvaliacao } from "../../services/avaliacoes";
import useModerador from "../../hooks/useModerador";
import CardAvaliacao from "../../components/CardAvaliacao";
import FiltroStatusAvaliacao from "../../components/FiltroStatusAvaliacao";
import "../pontos/detalhes.css";

function AvaliacoesPontoPagina() {
    const navigate = useNavigate();

    const { id } = useParams();

    const moderador = useModerador();

    const [dados, setDados] = useState(null);
    const [filtroStatus, setFiltroStatus] = useState("");
    const [recarregar, setRecarregar] = useState(0);

    useEffect(() => {
        if (moderador === null) {
            return;
        }

        async function carregarAvaliacoes() {
            try {
                const params = {};

                if (!moderador) {
                    params.status = "aprovado";
                } else if (filtroStatus) {
                    params.status = filtroStatus;
                }

                const res = await api.get(`/api/avaliacoes/ponto/${id}`, { params });

                setDados(res.data);
            } catch (error) {
                if (error.response?.status == 404) {
                    navigate("/erro", { replace: true });
                    return;
                }

                mostrarMensagem(mensagemDeErro(error), "danger");
            }
        }

        carregarAvaliacoes();
    }, [id, moderador, filtroStatus, recarregar])

    async function excluir(email, username) {
        if (await excluirAvaliacao(id, email, username)) {
            setRecarregar(recarregar + 1);
        }
    }

    async function alterarStatus(avaliacao, status) {
        if (await alterarStatusAvaliacao(id, avaliacao, status)) {
            setRecarregar(recarregar + 1);
        }
    }

    return (
        <>
            <div className="mt-4 pagina-avaliacoes">
                <div className="d-flex justify-content-between align-items-center mb-4">
                    <h2 className="mb-0">
                        {dados ? (<>Avaliações de <strong>{dados.ponto_nome}</strong></>) : "Avaliações"}
                    </h2>

                    <div>
                        {moderador && <FiltroStatusAvaliacao filtro={filtroStatus} onSelecionar={setFiltroStatus} />}
                    </div>
                </div>

                {dados && (
                    <>
                        <div>
                            {dados.logado && dados.avaliacao_usuario && (
                                <CardAvaliacao avaliacao={dados.avaliacao_usuario} idPonto={id} souVoce aoExcluir={excluir} />
                            )}
                        </div>

                        <div>
                            {!dados.avaliacoes || dados.avaliacoes.length == 0 ? (
                                <div className="alert alert-secondary text-center">Nenhuma avaliação encontrada!</div>
                            ) : (
                                dados.avaliacoes.map(avaliacao => (
                                    <CardAvaliacao key={avaliacao.usuario.email} avaliacao={avaliacao} idPonto={id}
                                        usuarioAdmin={dados.usuario_admin} aoExcluir={excluir} aoAlterarStatus={alterarStatus} />
                                ))
                            )}
                        </div>
                    </>
                )}

                <Link to={`/pontos/${id}`} className="btn btn-secondary mt-3">Voltar</Link>
            </div>
        </>
    )
}

export default AvaliacoesPontoPagina;
