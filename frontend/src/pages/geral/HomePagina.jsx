import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import CardPonto from "../../components/CardPonto";
import Alerta from "../../components/Alerta";

function HomePagina() {
    const [dados, setDados] = useState({logado: false, top_pontos: [], pontos_promocao: []});
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarIndex() {
            try {
                setErro(null);
                const res = await api.get("/api/pontos/index");
                setDados(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            }
        }
        carregarIndex();
    }, [])

    return (
        <>
            <div className="text-center mb-5">
                <h1 className="fw-bold">Explore o Mundo</h1>
                <p className="text-muted">Os melhores destinos para sua próxima aventura</p>
            </div>

            <Alerta mensagem={erro} />

            {dados.top_pontos.length > 0 && (
                <div>
                    <div className="secao-titulo text-center"><h3>Pontos Melhores Avaliados</h3></div>
                    <div className="row mb-5">
                        {dados.top_pontos.map((ponto, indice) => (
                            <CardPonto ponto={ponto} logado={dados.logado} ranking={indice + 1} key={ponto.id} />
                        ))}
                    </div>
                </div>
            )}

            {dados.pontos_promocao.length > 0 && (
                <div>
                    <div className="secao-titulo text-center"><h3>Pontos em Promoção</h3></div>
                    <div className="row">
                        {dados.pontos_promocao.map(ponto => (
                            <CardPonto ponto={ponto} logado={dados.logado} key={ponto.id} />
                        ))}
                    </div>
                </div>
            )}
        </>
    )
}

export default HomePagina;
