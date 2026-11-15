import { NavLink, useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import PontoForm from "../../components/PontoForm";

function PontoCadastro() {
    const navigate = useNavigate();

    async function salvar(dados) {
        const res = await api.post("/api/pontos", dados);

        // volta para a lista e mostra a mensagem do backend como toast
        navigate("/admin/pontos", {state: {mensagem: res.data.mensagem, classe: res.data.classe}});
    }

    const avisoSemCategoria = (
        <div className="card p-4 mb-4 shadow">
            <div className="alert alert-info text-center mb-3">
                Você precisa cadastrar uma categoria antes de criar um ponto turístico.
            </div>

            <NavLink to="/admin/categorias/cadastrar" className="btn btn-primary w-100">
                Cadastrar Categoria
            </NavLink>
        </div>
    );

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Cadastrar Ponto Turístico" />

                <PontoForm textoBotao="Adicionar" rotaVoltar="/admin/pontos" avisoSemCategoria={avisoSemCategoria} onSalvar={salvar} />
            </div>
        </>
    )
}

export default PontoCadastro;
