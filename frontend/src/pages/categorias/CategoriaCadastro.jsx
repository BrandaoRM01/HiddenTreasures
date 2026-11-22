import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import CategoriaForm from "../../components/CategoriaForm";

function CategoriaCadastro() {
    const navigate = useNavigate();

    async function salvar(dados) {
        const res = await api.post("/api/categorias", dados);

        navigate("/admin/categorias", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Cadastrar Categoria" />
                <CategoriaForm textoBotao="Adicionar" onSalvar={salvar} />
            </div>
        </>
    )
}

export default CategoriaCadastro;
