import { useEffect, useState } from "react";
import { NavLink, useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro, urlEstatico } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import { alterarStatusAvaliacao, excluirAvaliacao } from "../../services/avaliacoes";
import useModerador from "../../hooks/useModerador";
import Alerta from "../../components/Alerta";
import EstrelasNota from "../../components/EstrelasNota";
import CardAvaliacao from "../../components/CardAvaliacao";
import FiltroStatusAvaliacao from "../../components/FiltroStatusAvaliacao";
import "./detalhes.css";

function capitalizar(texto) {
    return texto.charAt(0).toUpperCase() + texto.slice(1);
}

// as datas da promoção chegam como YYYY-MM-DD; formatar pela string evita o "dia a menos" do new Date() no fuso do Brasil
function formatarDataSimples(dataIso) {
    const [ano, mes, dia] = dataIso.slice(0, 10).split("-");
    return `${dia}/${mes}/${ano}`;
}

function Linha({rotulo, valor}) {
    return (<p><strong>{rotulo}: </strong>{valor}</p>);
}

function BlocoPromocao({promocao, custoEntrada}) {
    return (
        <div className="mt-2 p-3" style={{backgroundColor: "#f8f9fa", borderLeft: "4px solid #d63384", borderRadius: "8px"}}>
            <h5 className="mb-1"><strong>{promocao.titulo}</strong></h5>

            <p className="mb-1">{promocao.descricao || "Sem descrição"}</p>

            <p style={{fontSize: "0.9rem", color: "#555", marginTop: "4px"}}>
                Promoção válida de {formatarDataSimples(promocao.data_inicio)} até {formatarDataSimples(promocao.data_fim)}
            </p>

            <p className="mb-0">
                {custoEntrada ? (
                    <>
                        <span style={{textDecoration: "line-through", color: "#999"}}>R$ {custoEntrada.toFixed(2)}</span>
                        <span style={{color: "#d63384", fontWeight: "bold"}}> R$ {(custoEntrada * (1 - Number(promocao.desconto) / 100)).toFixed(2)}</span>
                    </>
                ) : (
                    <span style={{color: "#d63384", fontWeight: "bold"}}>Gratuito</span>
                )}
            </p>
        </div>
    )
}

function DetalhesPontoPagina() {
    const navigate = useNavigate();

    const { id } = useParams();

    const moderador = useModerador();

    const [ponto, setPonto] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    const [dadosAvaliacoes, setDadosAvaliacoes] = useState(null);
    const [filtroStatus, setFiltroStatus] = useState("");
    const [recarregar, setRecarregar] = useState(0);

    // formulário "Avaliar este lugar"
    const [nota, setNota] = useState("");
    const [comentario, setComentario] = useState("");

    useEffect(() => {
        async function carregarPonto() {
            try {
                setErro(null);
                setCarregando(true);

                const res = await api.get(`/api/pontos/detalhes/${id}`);
                setPonto(res.data);
            }
            catch (error) {
                // ponto inexistente: volta para a lista, como no sistema atual
                if(error.response) {
                    navigate("/pontos", {replace: true});
                    return;
                }

                setErro(mensagemDeErro(error));
            }
            finally {
                setCarregando(false);
            }
        }

        carregarPonto();
    }, [id])

    // avaliações (só de ponto aprovado). Quem não é admin só recebe as aprovadas
    useEffect(() => {
        if(!ponto || ponto.status != "aprovado" || moderador === null) {
            return;
        }

        async function carregarAvaliacoes() {
            try {
                const params = moderador ? {} : {status: "aprovado"};
                const res = await api.get(`/api/avaliacoes/ponto/${id}`, {params});

                setDadosAvaliacoes(res.data);
            } catch (error) {
                // sem as avaliações a página continua funcionando, só não mostra a seção
            }
        }

        carregarAvaliacoes();
    }, [ponto, moderador, id, recarregar])

    async function enviarAvaliacao(e) {
        e.preventDefault();

        if(!nota) {
            mostrarMensagem("Selecione uma nota antes de enviar.", "danger");
            return;
        }

        try {
            const res = await api.post(`/api/avaliacoes/ponto/${id}`, {nota, comentario});

            mostrarMensagem(res.data.mensagem, res.data.classe);
            setRecarregar(recarregar + 1);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    async function excluir(email, username) {
        if(await excluirAvaliacao(id, email, username)) {
            setRecarregar(recarregar + 1);
        }
    }

    async function alterarStatus(avaliacao, status) {
        if(await alterarStatusAvaliacao(id, avaliacao, status)) {
            setRecarregar(recarregar + 1);
        }
    }

    function renderizarImagem() {
        return (
            <div className="position-relative">
                {ponto.promocao && (
                    <span style={{position: "absolute", top: "10px", left: "10px", backgroundColor: "#d63384", color: "white",
                        padding: "5px 10px", borderRadius: "8px", fontWeight: "bold", zIndex: 2}}>
                        -{Math.trunc(Number(ponto.promocao.desconto))}%
                    </span>
                )}

                <img src={urlEstatico(ponto.url_imagem)} alt={ponto.nome} className="img-fluid" />

                {ponto.destaques && ponto.destaques.length > 0 && (
                    <div className="position-absolute bottom-0 start-0 w-100 p-2 d-flex flex-wrap gap-1"
                        style={{background: "linear-gradient(to top, rgba(0,0,0,0.65), transparent)"}}>
                        {ponto.destaques.map(destaque => (
                            <span key={destaque.id} className="badge bg-dark bg-opacity-75 text-white">#{destaque.nome}</span>
                        ))}
                    </div>
                )}
            </div>
        )
    }

    function renderizarInfo() {
        const custoEntrada = Number(ponto.custo_entrada);

        return (
            <>
                <h2><strong>{ponto.nome}</strong></h2>

                <Linha rotulo="Tipo" valor={`Ponto ${capitalizar(ponto.tipo_ponto)}`} />
                <Linha rotulo="Localização" valor={ponto.localizacao} />
                <Linha rotulo="Descrição" valor={ponto.descricao} />

                {ponto.horario_funcionamento && <Linha rotulo="Horário de Funcionamento" valor={ponto.horario_funcionamento} />}

                <Linha rotulo="Categoria" valor={ponto.categoria.nome} />

                {ponto.tipo_ponto == "cultural" && (
                    <>
                        <Linha rotulo="Tipo Cultural" valor={ponto.tipo_cultural ? ponto.tipo_cultural.nome : "Não informado"} />
                        <Linha rotulo="Ano de Fundação" valor={ponto.ano_fundacao || "Não informado"} />
                    </>
                )}

                {ponto.tipo_ponto == "natural" && (
                    <>
                        <Linha rotulo="Ecossistema" valor={ponto.ecossistema ? ponto.ecossistema.nome : "Não informado"} />
                        <Linha rotulo="Área" valor={ponto.area_km ? `${ponto.area_km} km²` : "Não informada"} />
                    </>
                )}

                {ponto.promocao ? (
                    <BlocoPromocao promocao={ponto.promocao} custoEntrada={custoEntrada} />
                ) : (
                    <Linha rotulo="Custo de Entrada" valor={custoEntrada > 0 ? `R$ ${custoEntrada.toFixed(2)}` : "Gratuito"} />
                )}
            </>
        )
    }

    function renderizarSecaoAvaliar() {
        if(ponto.status != "aprovado") {
            return null;
        }

        if(!ponto.logado) {
            return (
                <div className="alert alert-info text-center mb-4">
                    Faça <NavLink className="alert-link" to="/login">login</NavLink> para avaliar este lugar.
                </div>
            );
        }

        return (
            <div className="card shadow-sm mb-4">
                <div className="card-body">
                    <h5 className="mb-3">Avaliar este lugar</h5>

                    <form onSubmit={enviarAvaliacao}>
                        <div className="mb-3">
                            <label className="form-label">Nota <span className="text-danger">*</span></label>
                            <EstrelasNota valor={nota} onChange={setNota} />
                        </div>

                        <div className="mb-3">
                            <label className="form-label" htmlFor="comentario">Comentário</label>
                            <textarea id="comentario" className="form-control" rows="3" placeholder="Compartilhe sua experiência..."
                                value={comentario} onChange={(e) => setComentario(e.target.value)}></textarea>
                        </div>

                        <button type="submit" className="btn btn-primary">Enviar avaliação</button>
                    </form>
                </div>
            </div>
        )
    }

    function renderizarAvaliacoes() {
        if(ponto.status != "aprovado" || !dadosAvaliacoes) {
            return null;
        }

        const { avaliacoes, avaliacao_usuario, usuario_admin } = dadosAvaliacoes;

        const quantidade = avaliacoes.length + (avaliacao_usuario ? 1 : 0);

        const filtradas = (moderador && filtroStatus) ? avaliacoes.filter(a => a.status == filtroStatus) : avaliacoes;
        const preview = filtradas.slice(0, 5);

        return (
            <div>
                <div className="mb-3 d-flex justify-content-between align-items-center">
                    <h4 className="fw-bold">Avaliações</h4>

                    {(moderador || quantidade >= 5) && (
                        <div className="d-flex gap-2 align-items-center">
                            {moderador && <FiltroStatusAvaliacao filtro={filtroStatus} onSelecionar={setFiltroStatus} />}

                            {quantidade >= 5 && (
                                <NavLink to={`/pontos/${id}/avaliacoes`} className="btn btn-outline-primary btn-sm">Ver mais</NavLink>
                            )}
                        </div>
                    )}
                </div>

                {avaliacao_usuario && (
                    <CardAvaliacao avaliacao={avaliacao_usuario} idPonto={id} souVoce aoExcluir={excluir} />
                )}

                {preview.length == 0 && !avaliacao_usuario ? (
                    <div className="alert alert-secondary text-center">
                        {filtroStatus ? "Nenhuma avaliação encontrada para esse filtro." : "Nenhuma avaliação ainda. Seja o primeiro!"}
                    </div>
                ) : (
                    preview.map(avaliacao => (
                        <CardAvaliacao key={avaliacao.usuario.email} avaliacao={avaliacao} idPonto={id} usuarioAdmin={usuario_admin}
                            aoExcluir={excluir} aoAlterarStatus={alterarStatus} />
                    ))
                )}
            </div>
        )
    }

    return (
        <>
            <div className="mt-4 pagina-detalhes">
                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {ponto && (
                    <>
                        <div className="row mb-4">
                            <div className="col-md-6">
                                {renderizarImagem()}
                            </div>

                            <div className="col-md-6 d-flex flex-column justify-content-center">
                                {renderizarInfo()}
                            </div>
                        </div>

                        <div>{renderizarSecaoAvaliar()}</div>
                        {renderizarAvaliacoes()}
                    </>
                )}
            </div>
        </>
    )
}

export default DetalhesPontoPagina;
