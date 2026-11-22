import { NavLink } from "react-router-dom";
import { urlEstatico } from "../services/api";
import Dropdown from "./Dropdown";
import BadgeAvaliacao from "./BadgeAvaliacao";

function formatarData(dataIso) {
    const data = new Date(dataIso);

    return `${data.toLocaleDateString("pt-BR")} ${data.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}`;
}

function CardAvaliacao({ avaliacao, idPonto, souVoce = false, usuarioAdmin = false, aoExcluir, aoAlterarStatus }) {
    const usuario = avaliacao.usuario;

    return (
        <>
            <div className={souVoce ? "card shadow-sm mb-3 border-primary" : "card shadow-sm mb-3"}>
                <div className="card-body">

                    <div className="d-flex justify-content-between align-items-start">
                        <div className="d-flex align-items-center mb-2">
                            <img src={urlEstatico(usuario.url_foto)} alt={usuario.username} className="rounded-circle me-2"
                                width="40" height="40" style={{ objectFit: "cover" }} />

                            <div>
                                <strong>{souVoce ? `${usuario.username} (Você)` : usuario.username}</strong><br />
                                <small className="text-muted">{formatarData(avaliacao.data_avaliacao)}</small>
                            </div>
                        </div>

                        {souVoce && (
                            <div className="d-flex gap-2">
                                <NavLink to={`/pontos/${idPonto}/avaliacao/editar`} title="Editar"
                                    className="btn btn-warning btn-sm d-flex align-items-center justify-content-center">
                                    <i className="bi bi-pencil"></i>
                                </NavLink>

                                <button type="button" title="Excluir" onClick={() => aoExcluir(usuario.email)}
                                    className="btn btn-danger btn-sm d-flex align-items-center justify-content-center">
                                    <i className="bi bi-trash"></i>
                                </button>
                            </div>
                        )}

                        {!souVoce && usuarioAdmin && (
                            <div className="d-flex gap-2">
                                {avaliacao.status == "pendente" && (
                                    <Dropdown classeBotao="btn btn-sm btn-light" rotuloBotao={<i className="bi bi-three-dots-vertical"></i>}
                                        itens={[
                                            { texto: "Aprovar", classe: "text-success", onClick: () => aoAlterarStatus(avaliacao, "aprovado") },
                                            {
                                                texto: "Rejeitar", classe: "text-danger", onClick: () => {
                                                    if (window.confirm(`Deseja realmente rejeitar a avaliação de ${usuario.username}?`)) {
                                                        aoAlterarStatus(avaliacao, "rejeitado");
                                                    }
                                                }
                                            },
                                        ]} />
                                )}

                                <button type="button" title="Excluir" onClick={() => aoExcluir(usuario.email, usuario.username)}
                                    className="btn btn-danger btn-sm d-flex align-items-center justify-content-center">
                                    <i className="bi bi-trash"></i>
                                </button>
                            </div>
                        )}
                    </div>

                    <div className="d-flex justify-content-between align-items-center mb-1">
                        <p className="text-warning mb-0">{"⭐".repeat(avaliacao.nota)}</p>

                        {(souVoce || usuarioAdmin) && <BadgeAvaliacao status={avaliacao.status} />}
                    </div>

                    {avaliacao.comentario && <p>{avaliacao.comentario}</p>}

                </div>
            </div>
        </>
    )
}

export default CardAvaliacao;
