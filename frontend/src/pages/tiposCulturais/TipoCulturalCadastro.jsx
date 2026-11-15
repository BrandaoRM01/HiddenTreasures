import { useNavigate } from "react-router-dom";
import { api } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import TipoCulturalForm from "../../components/TipoCulturalForm";

function TipoCulturalCadastro() {
    const navigate = useNavigate();

    async function salvar(dados) {
        const res = await api.post("/api/tipos_culturais", dados);

        // volta para a lista e mostra a mensagem do backend como toast
        navigate("/admin/tipos-culturais", {state: {mensagem: res.data.mensagem, classe: res.data.classe}});
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Cadastrar Tipo Cultural" />
                <TipoCulturalForm textoBotao="Adicionar" onSalvar={salvar} />
            </div>
        </>
    )
}

export default TipoCulturalCadastro;
