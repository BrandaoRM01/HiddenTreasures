import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import PromocaoForm from "../../components/PromocaoForm";

function PromocaoCadastro() {
    const navigate = useNavigate();

    async function salvar(dados) {
        const res = await api.post("/api/promocoes", dados);

        navigate("/admin/promocoes", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Cadastrar Promoção" />
                <PromocaoForm textoBotao="Adicionar" onSalvar={salvar} />
            </div>
        </>
    )
}

export default PromocaoCadastro;
