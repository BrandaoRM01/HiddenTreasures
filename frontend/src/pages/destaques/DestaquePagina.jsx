import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import Filtro from "../../components/Filtro";
import LinhaLista from "../../components/LinhaLista";
import ListaVazia from "../../components/ListaVazia";

function DestaquePagina() {
    const [busca, setBusca] = useState("");
    const [destaques, setDestaques] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarDestaques() {
            try {
                setErro(null);
                const res = await api.get("/api/destaques");
                setDestaques(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarDestaques();
    }, [])

    let listaFiltrada = destaques.filter(i => i.nome.toLowerCase().includes(busca.toLowerCase()));

    async function excluir(item) {
        if(!window.confirm(`Tem certeza que deseja excluir o destaque ${item.nome}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/destaques/${item.id}`);

            setDestaques(destaques.filter(i => i.id != item.id));
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

        if(destaques.length == 0) {
            return (
                <ListaVazia
                    icone="bi-star-fill"
                    titulo="Nenhum destaque cadastrado"
                    texto="Comece criando um destaque para os pontos turísticos."
                    rota="/admin/destaques/cadastrar"
                    textoBotao="Criar primeiro destaque"
                />
            );
        }

        if(listaFiltrada.length == 0) {
            return (<p className="text-muted text-center py-4 mb-0">Nenhum resultado para a busca.</p>);
        }

        return listaFiltrada.map(item => (
            <LinhaLista key={item.id} rotaEditar={`/admin/destaques/${item.id}/atualizar`} onExcluir={() => excluir(item)}>
                <div>
                    <strong>{item.nome}</strong>
                </div>
            </LinhaLista>
        ));
    }

    return (
        <>
            <LayoutLista
                titulo="Gerenciar Destaques"
                erro={erro}
                acao={destaques.length > 0 && <NavLink className="btn btn-primary" to="/admin/destaques/cadastrar">Novo destaque</NavLink>}
                filtro={destaques.length > 0 && <Filtro busca={busca} onBuscaChange={setBusca} />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default DestaquePagina;
