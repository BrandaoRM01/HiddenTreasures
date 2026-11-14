import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import Secao from "../../components/Secao";
import CardPonto from "../../components/CardPonto";
import Alerta from "../../components/Alerta";

function FavoritoPagina() {
    const [pontos, setPontos] = useState([]);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarFavoritos() {
            try {
                setErro(null);
                const res = await api.get("/api/usuarios/favoritos");
                setPontos(res.data.map(ponto => ({ ...ponto, favorito: true })));
            } catch (error) {
                setErro(mensagemDeErro(error));
            }
        }
        carregarFavoritos();
    }, [])

    function removerDaLista(idPonto, favorito) {
        if (!favorito) {
            setPontos(pontos.filter(p => p.id != idPonto));
        }
    }

    return (
        <>
            <Secao titulo="Meus Favoritos">
                <Alerta mensagem={erro} />

                {pontos.length == 0 && !erro ? (
                    <p className="text-muted">
                        Você ainda não favoritou nenhum ponto. <NavLink to="/pontos">Ver pontos turísticos</NavLink>
                    </p>
                ) : (
                    <div className="row">
                        {pontos.map(ponto => (
                            <CardPonto ponto={ponto} logado={true} onFavoritoAlterado={removerDaLista} key={ponto.id} />
                        ))}
                    </div>
                )}
            </Secao>
        </>
    )
}

export default FavoritoPagina;
