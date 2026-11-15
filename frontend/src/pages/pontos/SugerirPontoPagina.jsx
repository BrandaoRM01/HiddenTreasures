import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import TituloAdmin from "../../components/TituloAdmin";
import PontoForm from "../../components/PontoForm";
import CartaoPontoAdmin from "../../components/CartaoPontoAdmin";
import Alerta from "../../components/Alerta";

function SugerirPontoPagina() {
    const [sugestoes, setSugestoes] = useState([]);
    const [recarregar, setRecarregar] = useState(0);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarSugestoes() {
            try {
                setErro(null);
                const res = await api.get("/api/pontos/minhas-sugestoes");
                setSugestoes(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarSugestoes();
    }, [recarregar])

    // o backend cadastra como "pendente" (quem não é admin só consegue sugerir)
    async function sugerir(dados) {
        const res = await api.post("/api/pontos", dados);

        setRecarregar(recarregar + 1);
        mostrarMensagem(res.data.mensagem, res.data.classe);
    }

    async function excluir(ponto) {
        if(!window.confirm(`Tem certeza que deseja excluir a sugestão ${ponto.nome}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/pontos/${ponto.id}`);

            setSugestoes(sugestoes.filter(s => s.id != ponto.id));
            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    const avisoSemCategoria = (
        <div className="card p-4 mb-4 shadow">
            <div className="alert alert-info text-center mb-0">
                Sem uma categoria você não pode sugerir um ponto turístico. Aguarde até que um administrador adicione
                categorias para sugerir pontos turísticos.
            </div>
        </div>
    );

    function renderizarLista() {
        if(carregando) {
            return (<p className="text-muted mb-0">Carregando...</p>);
        }

        if(erro) {
            return null;
        }

        if(sugestoes.length == 0) {
            return (
                <div className="text-center py-5">
                    <i className="bi bi-map display-1 text-secondary"></i>
                    <h3 className="mt-3">Nenhum ponto sugerido por você</h3>
                    <p className="text-muted">Comece sugerindo um ponto turístico para a comunidade.</p>
                </div>
            );
        }

        return (
            <div className="row g-3">
                {sugestoes.map(ponto => (
                    <CartaoPontoAdmin ponto={ponto} key={ponto.id} classeCartao="card border shadow-sm"
                        classeBotoes="d-flex flex-wrap justify-content-lg-end gap-2"
                        detalhes={
                            <>
                                {ponto.promocao && ponto.promocao.titulo && (
                                    <p className="mb-1"><strong>Promoção:</strong> {ponto.promocao.titulo}</p>
                                )}

                                {ponto.media_avaliacao != null && (
                                    <p className="mb-0 text-warning">⭐ {Number(ponto.media_avaliacao).toFixed(1)}</p>
                                )}
                            </>
                        }>

                        {(ponto.status == "pendente" || ponto.status == "rejeitado") ? (
                            <>
                                <NavLink className="btn btn-warning" to={`/sugestoes/${ponto.id}/editar`}>
                                    <i className="bi bi-pencil-fill"></i>
                                </NavLink>

                                <button type="button" className="btn btn-danger" onClick={() => excluir(ponto)}>
                                    <i className="bi bi-trash-fill"></i>
                                </button>
                            </>
                        ) : (
                            <button type="button" className="btn btn-outline-secondary" disabled>
                                <i className="bi bi-lock-fill"></i> Sugestão Aprovada
                            </button>
                        )}
                    </CartaoPontoAdmin>
                ))}
            </div>
        );
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Sugerir Pontos Turísticos" />

                <PontoForm textoBotao="Adicionar" limparAposSalvar avisoSemCategoria={avisoSemCategoria} onSalvar={sugerir} />

                <div className="card shadow-sm border-0">
                    <div className="card-header bg-white">
                        <h4 className="mb-0">Minhas Sugestões</h4>
                    </div>

                    <div className="card-body">
                        <Alerta mensagem={erro} />
                        {renderizarLista()}
                    </div>
                </div>
            </div>
        </>
    )
}

export default SugerirPontoPagina;
