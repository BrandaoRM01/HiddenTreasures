import { useState } from "react";
import { NavLink } from "react-router-dom";
import { api, mensagemDeErro, urlEstatico } from "../services/api";
import { mostrarMensagem } from "../services/mensagem";

function classeRanking(posicao) {
    if(posicao == 1) return "gold";
    if(posicao == 2) return "silver";
    if(posicao == 3) return "bronze";
    return "blue";
}

// Card de ponto turístico (Home, Pontos e Favoritos).
//   logado:             mostra o coração de favorito
//   ranking:            posição no top (mostra o número ouro/prata/bronze/azul sobre a imagem)
//   onFavoritoAlterado: (idPonto, favorito) => void
function CardPonto({ponto, logado, ranking, onFavoritoAlterado}) {
    const [favorito, setFavorito] = useState(Boolean(ponto.favorito));

    const tipo = ponto.tipo_ponto.charAt(0).toUpperCase() + ponto.tipo_ponto.slice(1);
    const media = ponto.media_avaliacao !== null && ponto.media_avaliacao !== undefined ? Number(ponto.media_avaliacao) : null;
    const custoEntrada = Number(ponto.custo_entrada);

    async function alternarFavorito() {
        try {
            const res = favorito
                ? await api.delete(`/api/usuarios/favoritos/${ponto.id}`)
                : await api.post("/api/usuarios/favoritos", {ponto_id: ponto.id});

            setFavorito(!favorito);

            if(onFavoritoAlterado) {
                onFavoritoAlterado(ponto.id, !favorito);
            }

            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    function renderPreco() {
        if(!custoEntrada) {
            return <span className="preco-promocao">Gratuito</span>;
        }

        if(ponto.promocao) {
            const valorComDesconto = custoEntrada * (1 - Number(ponto.promocao.desconto) / 100);

            return (
                <>
                    <span className="preco-antigo">R$ {custoEntrada.toFixed(2)}</span>
                    <span className="preco-promocao">R$ {valorComDesconto.toFixed(2)}</span>
                </>
            );
        }

        return `R$ ${custoEntrada.toFixed(2)}`;
    }

    return (
        <>
            <div className="col-md-4 mb-4 d-flex">
                <div className="card shadow-sm card-hover card-ponto w-100 position-relative">
                    <div className="position-relative">
                        <img src={urlEstatico(ponto.url_imagem)} alt={ponto.nome} className="card-img-top rounded-top ponto-img" style={{height: "300px", objectFit: "cover"}} />

                        {ranking && (
                            <div className={`ranking-number ${classeRanking(ranking)}`}>{ranking}</div>
                        )}

                        {ponto.destaques && ponto.destaques.length > 0 && (
                            <div className="position-absolute bottom-0 start-0 w-100 p-2 d-flex flex-wrap gap-1"
                                style={{background: "linear-gradient(to top, rgba(0,0,0,0.6), transparent)"}}>
                                {ponto.destaques.map(destaque => (
                                    <span key={destaque.id} className="badge bg-dark bg-opacity-75 text-white">#{destaque.nome}</span>
                                ))}
                            </div>
                        )}

                        {ponto.promocao && (
                            <div className={ranking ? "badge-desconto-direita" : "badge-desconto"}>-{Math.trunc(Number(ponto.promocao.desconto))}%</div>
                        )}
                    </div>

                    <div className="card-body">
                        <div>
                            <h5>{ponto.nome}</h5>
                            <p className="text-muted">Ponto {tipo}</p>
                            <p className="text-muted localizacao">{ponto.localizacao}</p>
                            <p className="text-muted">{ponto.categoria.nome}</p>
                            <p className="text-warning">{media !== null ? `⭐ ${media.toFixed(1)}` : "⭐ Nenhuma avaliação"}</p>
                        </div>

                        <div className="d-flex justify-content-between align-items-center">
                            <p className="preco mb-0">{renderPreco()}</p>

                            {logado && (
                                <button type="button" onClick={alternarFavorito}
                                    className="btn btn-light rounded-circle shadow-sm d-flex align-items-center justify-content-center"
                                    style={{width: "40px", height: "40px"}}>
                                    <span style={{fontSize: "20px"}}>{favorito ? "❤️" : "🤍"}</span>
                                </button>
                            )}
                        </div>

                        <NavLink className="btn btn-primary w-100 mt-2" to={`/pontos/${ponto.id}`}>Ver detalhes</NavLink>
                    </div>
                </div>
            </div>
        </>
    )
}

export default CardPonto;
