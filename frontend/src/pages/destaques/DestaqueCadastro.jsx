import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import DestaqueForm from "../../components/DestaqueForm";

function DestaqueCadastro() {
    const navigate = useNavigate();

    async function salvar(dados) {
        const res = await api.post("/api/destaques", dados);

        navigate("/admin/destaques", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Cadastrar Destaque" />
                <DestaqueForm textoBotao="Adicionar" onSalvar={salvar} />
            </div>
        </>
    )
}

export default DestaqueCadastro;
