import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import FiltroPontos from "../../components/FiltroPontos";
import CartaoPontoAdmin from "../../components/CartaoPontoAdmin";

function filtrarSugestoes(lista, filtros) {
    const contem = (texto, trecho) => (texto ?? "").toLowerCase().includes(trecho.toLowerCase());

    return lista.filter(s =>
        (!filtros.busca || contem(s.nome, filtros.busca)) &&
        (!filtros.categoria || contem(s.categoria.nome, filtros.categoria)) &&
        (!filtros.tipo || s.tipo_ponto == filtros.tipo) &&
        (!filtros.localizacao || contem(s.localizacao, filtros.localizacao)) &&
        (!filtros.status || s.status == filtros.status)
    );
}

function SugestaoAdminPagina() {
    const [filtros, setFiltros] = useState({});
    const [recarregar, setRecarregar] = useState(0);
    const [sugestoes, setSugestoes] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarSugestoes() {
            try {
                setErro(null);
                const res = await api.get("/api/pontos/sugestoes");
                setSugestoes(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarSugestoes();
    }, [recarregar])

    let listaFiltrada = filtrarSugestoes(sugestoes, filtros);

    async function alterarStatus(ponto, status) {
        if (status == "rejeitado") {
            if (!window.confirm(`Deseja realmente rejeitar a sugestão ${ponto.nome}?`)) {
                return;
            }
        }

        const dados = new FormData();
        const texto = (valor) => String(valor ?? "");

        dados.append("nome", ponto.nome);
        dados.append("localizacao", ponto.localizacao);
        dados.append("descricao", ponto.descricao);
        dados.append("horario_funcionamento", texto(ponto.horario_funcionamento));
        dados.append("custo_entrada", texto(ponto.custo_entrada));
        dados.append("categoria", ponto.categoria.id);
        dados.append("tipo_ponto", ponto.tipo_ponto);
        dados.append("status", status);

        if (ponto.promocao) {
            dados.append("promocao", ponto.promocao.id);
        }

        if (ponto.tipo_ponto == "cultural") {
            if (ponto.tipo_cultural) {
                dados.append("tipo_cultural", ponto.tipo_cultural.id);
            }
            dados.append("ano_fundacao", texto(ponto.ano_fundacao));
        } else {
            if (ponto.ecossistema) {
                dados.append("ecossistema", ponto.ecossistema.id);
            }
            dados.append("area_km", texto(ponto.area_km));
        }

        (ponto.destaques || []).forEach(destaque => {
            dados.append("destaques", destaque.id);
        });

        try {
            const res = await api.put(`/api/pontos/${ponto.id}`, dados);

            setRecarregar(recarregar + 1);
            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    async function excluir(ponto) {
        if (!window.confirm(`Tem certeza que deseja excluir o ponto turístico ${ponto.nome}?`)) {
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

    function renderizarLista() {
        if (carregando) {
            return (<p className="text-muted mb-0">Carregando...</p>);
        }

        if (erro) {
            return null;
        }

        if (sugestoes.length == 0) {
            return (
                <div className="text-center py-5">
                    <i className="bi bi-check2-circle display-1 text-success"></i>
                    <h3 className="mt-3">Nenhuma sugestão pendente</h3>
                    <p className="text-muted mb-0">Todas as sugestões já foram analisadas.</p>
                </div>
            );
        }

        if (listaFiltrada.length == 0) {
            return (
                <div className="text-center py-5">
                    <i className="bi bi-geo-alt display-1 text-secondary"></i>
                    <h4 className="mb-2 mt-3">Nenhuma sugestão encontrada</h4>
                    <p className="text-muted mb-0">Ajuste os filtros para ver outras sugestões.</p>
                </div>
            );
        }

        return (
            <div className="row g-3">
                {listaFiltrada.map(ponto => (
                    <CartaoPontoAdmin ponto={ponto} key={ponto.id} classeBotoes="d-flex justify-content-lg-end justify-content-start gap-2"
                        detalhes={ponto.sugerido_por && (
                            <p className="mb-0"><strong>Sugerido por:</strong> {ponto.sugerido_por}</p>
                        )}>

                        <NavLink className="btn btn-primary" to={`/pontos/${ponto.id}`} title="Ver detalhes">
                            <i className="bi bi-eye-fill"></i>
                        </NavLink>

                        {ponto.status == "pendente" && (
                            <>
                                <button type="button" className="btn btn-success" title="Aprovar" onClick={() => alterarStatus(ponto, "aprovado")}>
                                    <i className="bi bi-check-lg"></i>
                                </button>

                                <button type="button" className="btn btn-rejeitar" title="Rejeitar" onClick={() => alterarStatus(ponto, "rejeitado")}>
                                    <i className="bi bi-x-lg"></i>
                                </button>
                            </>
                        )}

                        <button type="button" className="btn btn-danger" title="Excluir" onClick={() => excluir(ponto)}>
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
                titulo="Gerenciar Sugestões"
                subtitulo="Aprove ou rejeite sugestões enviadas pelos usuários."
                classeCard="p-3"
                erro={erro}
                filtro={<FiltroPontos onFiltrar={setFiltros} />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default SugestaoAdminPagina;
