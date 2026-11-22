import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import EcossistemaForm from "../../components/EcossistemaForm";

function EcossistemaCadastro() {
    const navigate = useNavigate();

    async function salvar(dados) {
        const res = await api.post("/api/ecossistemas", dados);

        navigate("/admin/ecossistemas", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Cadastrar Ecossistema" />
                <EcossistemaForm textoBotao="Adicionar" onSalvar={salvar} />
            </div>
        </>
    )
}

export default EcossistemaCadastro;
