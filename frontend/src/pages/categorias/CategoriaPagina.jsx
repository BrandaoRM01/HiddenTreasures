import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import Filtro from "../../components/Filtro";
import LinhaLista from "../../components/LinhaLista";
import ListaVazia from "../../components/ListaVazia";

function CategoriaPagina() {
    const [busca, setBusca] = useState("");
    const [categorias, setCategorias] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarCategorias() {
            try {
                setErro(null);
                const res = await api.get("/api/categorias");
                setCategorias(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarCategorias();
    }, [])

    let listaFiltrada = categorias.filter(i => i.nome.toLowerCase().includes(busca.toLowerCase()));

    async function excluir(item) {
        if(!window.confirm(`Tem certeza que deseja excluir a categoria ${item.nome}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/categorias/${item.id}`);

            setCategorias(categorias.filter(i => i.id != item.id));
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

        if(categorias.length == 0) {
            return (
                <ListaVazia
                    icone="bi-tags"
                    titulo="Nenhuma categoria cadastrada"
                    texto="Comece criando uma categoria para organizar os pontos turísticos."
                    rota="/admin/categorias/cadastrar"
                    textoBotao="Criar primeira categoria"
                />
            );
        }

        if(listaFiltrada.length == 0) {
            return (<p className="text-muted text-center py-4 mb-0">Nenhum resultado para a busca.</p>);
        }

        return listaFiltrada.map(item => (
            <LinhaLista key={item.id} rotaEditar={`/admin/categorias/${item.id}/atualizar`} onExcluir={() => excluir(item)}>
                <div>
                    <strong>{item.nome}</strong>
                    <br />
                    <small className="text-muted">{item.descricao}</small>
                </div>
            </LinhaLista>
        ));
    }

    return (
        <>
            <LayoutLista
                titulo="Gerenciar Categorias"
                erro={erro}
                acao={categorias.length > 0 && <NavLink className="btn btn-primary" to="/admin/categorias/cadastrar">Nova categoria</NavLink>}
                filtro={categorias.length > 0 && <Filtro busca={busca} onBuscaChange={setBusca} />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default CategoriaPagina;
