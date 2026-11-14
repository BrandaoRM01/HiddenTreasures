import { NavLink } from "react-router-dom";
import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import Filtro from "../../components/Filtro";
import LinhaLista from "../../components/LinhaLista";
import ListaVazia from "../../components/ListaVazia";

function TipoCulturalPagina() {
    const [busca, setBusca] = useState("");
    const [tiposCulturais, setTiposCulturais] = useState([]);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarTiposCulturais() {
            try {
                setErro(null);
                const res = await api.get("/api/tipos_culturais");
                setTiposCulturais(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarTiposCulturais();
    }, [])

    let listaFiltrada = tiposCulturais.filter(i => i.nome.toLowerCase().includes(busca.toLowerCase()));

    async function excluir(item) {
        if(!window.confirm(`Tem certeza que deseja excluir o tipo cultural ${item.nome}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/tipos_culturais/${item.id}`);

            setTiposCulturais(tiposCulturais.filter(i => i.id != item.id));
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

        if(tiposCulturais.length == 0) {
            return (
                <ListaVazia
                    icone="bi-palette"
                    titulo="Nenhum tipo cultural cadastrado"
                    texto="Comece criando um tipo cultural para classificar os pontos culturais."
                    rota="/admin/tipos-culturais/cadastrar"
                    textoBotao="Criar primeiro tipo cultural"
                />
            );
        }

        if(listaFiltrada.length == 0) {
            return (<p className="text-muted text-center py-4 mb-0">Nenhum resultado para a busca.</p>);
        }

        return listaFiltrada.map(item => (
            <LinhaLista key={item.id} rotaEditar={`/admin/tipos-culturais/${item.id}/atualizar`} onExcluir={() => excluir(item)}>
                <div>
                    <strong>{item.nome}</strong>
                </div>
            </LinhaLista>
        ));
    }

    return (
        <>
            <LayoutLista
                titulo="Gerenciar Tipos Culturais"
                erro={erro}
                acao={tiposCulturais.length > 0 && <NavLink className="btn btn-primary" to="/admin/tipos-culturais/cadastrar">Novo tipo cultural</NavLink>}
                filtro={tiposCulturais.length > 0 && <Filtro busca={busca} onBuscaChange={setBusca} />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default TipoCulturalPagina;
