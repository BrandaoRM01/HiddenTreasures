import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import Filtro from "../../components/Filtro";
import LinhaLista from "../../components/LinhaLista";
import ListaVazia from "../../components/ListaVazia";

function EcossistemaPagina() {
    const [busca, setBusca] = useState("");
    const [ecossistemas, setEcossistemas] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarEcossistemas() {
            try {
                setErro(null);
                const res = await api.get("/api/ecossistemas");
                setEcossistemas(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarEcossistemas();
    }, [])

    let listaFiltrada = ecossistemas.filter(i => i.nome.toLowerCase().includes(busca.toLowerCase()));

    async function excluir(item) {
        if(!window.confirm(`Tem certeza que deseja excluir o ecossistema ${item.nome}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/ecossistemas/${item.id}`);

            setEcossistemas(ecossistemas.filter(i => i.id != item.id));
            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    function renderizarLista() {
        if(carregando) {
            return (<p className="text-muted mb-0">Carregando...</p>);
        }

        if(erro) {
            return null;
        }

        if(ecossistemas.length == 0) {
            return (
                <ListaVazia
                    icone="bi-tree"
                    titulo="Nenhum ecossistema cadastrado"
                    texto="Comece criando um ecossistema para classificar os pontos naturais."
                    rota="/admin/ecossistemas/cadastrar"
                    textoBotao="Criar primeiro ecossistema"
                />
            );
        }

        if(listaFiltrada.length == 0) {
            return (<p className="text-muted text-center py-4 mb-0">Nenhum resultado para a busca.</p>);
        }

        return listaFiltrada.map(item => (
            <LinhaLista key={item.id} rotaEditar={`/admin/ecossistemas/${item.id}/atualizar`} onExcluir={() => excluir(item)}>
                <div>
                    <strong>{item.nome}</strong>
                </div>
            </LinhaLista>
        ));
    }

    return (
        <>
            <LayoutLista
                titulo="Gerenciar Ecossistemas"
                erro={erro}
                acao={ecossistemas.length > 0 && <NavLink className="btn btn-primary" to="/admin/ecossistemas/cadastrar">Novo ecossistema</NavLink>}
                filtro={ecossistemas.length > 0 && <Filtro busca={busca} onBuscaChange={setBusca} />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default EcossistemaPagina;
