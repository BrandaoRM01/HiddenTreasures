import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import CategoriaForm from "../../components/CategoriaForm";
import Alerta from "../../components/Alerta";

function CategoriaAtualizar() {
    const navigate = useNavigate();

    const { id } = useParams();

    const [categoria, setCategoria] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarCategoria() {
            try {
                setErro(null);
                setCarregando(true);

                const res = await api.get(`/api/categorias/${id}`);
                setCategoria(categoriaParaForm(res.data));
            }
            catch (error) {
                setErro(mensagemDeErro(error));
            }
            finally {
                setCarregando(false);
            }
        }

        carregarCategoria();
    }, [id])

    async function atualizar(dados) {
        const res = await api.put(`/api/categorias/${id}`, dados);

        navigate("/admin/categorias", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    function categoriaParaForm(categoria) {
        return {
            nome: categoria.nome,
            descricao: categoria.descricao ?? '',
        }
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Editar Categoria" />

                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {categoria && <CategoriaForm valorInicial={categoria} textoBotao="Salvar Alterações" onSalvar={atualizar} />}
            </div>
        </>
    )
}

export default CategoriaAtualizar;
