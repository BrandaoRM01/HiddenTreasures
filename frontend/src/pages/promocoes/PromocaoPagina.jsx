import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import Filtro from "../../components/Filtro";
import LinhaLista from "../../components/LinhaLista";
import ListaVazia from "../../components/ListaVazia";

function formatarData(data) {
    let [ano, mes, dia] = data.split("-");
    return `${dia}/${mes}/${ano}`;
}

function PromocaoPagina() {
    const [busca, setBusca] = useState("");
    const [promocoes, setPromocoes] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarPromocoes() {
            try {
                setErro(null);
                const res = await api.get("/api/promocoes");
                setPromocoes(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarPromocoes();
    }, [])

    let listaFiltrada = promocoes.filter(p => p.titulo.toLowerCase().includes(busca.toLowerCase()));

    async function excluir(promocao) {
        if (!window.confirm(`Tem certeza que deseja excluir a promoção ${promocao.titulo}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/promocoes/${promocao.id}`);

            setPromocoes(promocoes.filter(p => p.id != promocao.id));
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

        if (promocoes.length == 0) {
            return (
                <ListaVazia
                    icone="bi-tags"
                    titulo="Nenhuma promoção cadastrada"
                    texto="Comece cadastrando uma promoção para aplicar aos pontos turísticos."
                    rota="/admin/promocoes/cadastrar"
                    textoBotao="Cadastrar primeira promoção"
                />
            );
        }

        if (listaFiltrada.length == 0) {
            return (<p className="text-muted text-center py-4 mb-0">Nenhum resultado para a busca.</p>);
        }

        return listaFiltrada.map(promocao => (
            <LinhaLista key={promocao.id} rotaEditar={`/admin/promocoes/${promocao.id}/atualizar`} onExcluir={() => excluir(promocao)}>
                <div>
                    <strong>{promocao.titulo}</strong>
                    <br />
                    {promocao.descricao && (
                        <>
                            <small className="text-muted">{promocao.descricao}</small>
                            <br />
                        </>
                    )}
                    <small className="text-muted">{promocao.desconto}% de desconto</small>
                    <br />
                    <small className="text-muted">{formatarData(promocao.data_inicio)} até {formatarData(promocao.data_fim)}</small>
                </div>
            </LinhaLista>
        ));
    }

    return (
        <>
            <LayoutLista
                titulo="Gerenciar Promoções"
                classeCard="p-3"
                erro={erro}
                acao={promocoes.length > 0 && <NavLink className="btn btn-primary" to="/admin/promocoes/cadastrar">Nova promoção</NavLink>}
                filtro={promocoes.length > 0 && <Filtro busca={busca} onBuscaChange={setBusca} placeholder="Buscar por título" />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default PromocaoPagina;
