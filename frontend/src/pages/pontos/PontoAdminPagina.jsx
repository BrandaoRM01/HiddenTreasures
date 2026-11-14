import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import FiltroPontos from "../../components/FiltroPontos";
import CartaoPontoAdmin from "../../components/CartaoPontoAdmin";
import Paginacao from "../../components/Paginacao";

function PontoAdminPagina() {
    const [filtros, setFiltros] = useState({});
    const [pagina, setPagina] = useState(1);
    const [recarregar, setRecarregar] = useState(0);
    const [pontos, setPontos] = useState([]);
    const [paginacao, setPaginacao] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    // busca e paginação são feitas pela API; só consulta de novo ao clicar em "Filtrar" ou trocar de página
    useEffect(() => {
        async function carregarPontos() {
            try {
                setErro(null);

                const params = { page: pagina, limit: 10 };

                Object.entries(filtros).forEach(([chave, valor]) => {
                    if (valor) params[chave] = valor;
                });

                const res = await api.get("/api/pontos", { params });

                // apagou o último ponto de uma página que não é a primeira: volta uma página
                if (res.data.pontos.length == 0 && pagina > 1) {
                    setPagina(pagina - 1);
                    return;
                }

                setPontos(res.data.pontos);
                setPaginacao(res.data.paginacao);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarPontos();
    }, [filtros, pagina, recarregar])

    function aplicarFiltros(valores) {
        setFiltros(valores);
        setPagina(1);
    }

    async function excluir(ponto) {
        if (!window.confirm(`Tem certeza que deseja excluir o ponto turístico ${ponto.nome}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/pontos/${ponto.id}`);

            setRecarregar(recarregar + 1);
            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    function renderizarLista() {
        if (carregando) {
            return (<p className="text-muted mb-0">Carregando...</p>);
        }

        if (erro) {
            return null;
        }

        if (pontos.length == 0) {
            return (
                <div className="text-center py-5">
                    <i className="bi bi-geo-alt display-1 text-secondary"></i>
                    <h4 className="mb-2 mt-3">Nenhum ponto encontrado</h4>
                    <p className="text-muted">Ajuste os filtros ou cadastre um novo ponto turístico.</p>
                </div>
            );
        }

        return (
            <div className="row g-3">
                {pontos.map(ponto => (
                    <CartaoPontoAdmin ponto={ponto} key={ponto.id} classeBotoes="d-flex flex-wrap justify-content-lg-end gap-2"
                        detalhes={
                            <>
                                {ponto.promocao && ponto.promocao.titulo ? (
                                    <p className="mb-1"><strong>Promoção:</strong> {ponto.promocao.titulo}</p>
                                ) : (
                                    <p className="mb-1 text-muted">Nenhuma promoção ativa</p>
                                )}

                                {ponto.media_avaliacao !== null && ponto.media_avaliacao !== undefined ? (
                                    <span className="badge text-warning">⭐ {Number(ponto.media_avaliacao).toFixed(1)}</span>
                                ) : (
                                    <span className="badge bg-secondary">Sem avaliações</span>
                                )}
                            </>
                        }>

                        {ponto.status == "aprovado" && (
                            <NavLink className="btn btn-warning" to={`/admin/pontos/${ponto.id}/atualizar`}>
                                <i className="bi bi-pencil-fill"></i>
                            </NavLink>
                        )}

                        <button type="button" className="btn btn-danger" onClick={() => excluir(ponto)}>
                            <i className="bi bi-trash-fill"></i>
                        </button>
                    </CartaoPontoAdmin>
                ))}
            </div>
        );
    }

    return (
        <>
            <LayoutLista
                titulo="Gerenciar Pontos Turísticos"
                classeCard="p-3"
                erro={erro}
                acao={<NavLink className="btn btn-primary" to="/admin/pontos/cadastrar">Novo ponto</NavLink>}
                filtro={<FiltroPontos onFiltrar={aplicarFiltros} />}
                rodape={<Paginacao paginacao={paginacao} onMudar={setPagina} />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default PontoAdminPagina;
