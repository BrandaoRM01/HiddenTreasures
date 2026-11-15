import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import TipoCulturalForm from "../../components/TipoCulturalForm";
import Alerta from "../../components/Alerta";

function TipoCulturalAtualizar() {
    const navigate = useNavigate();

    const { id } = useParams();

    const [tipoCultural, setTipoCultural] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarTipoCultural() {
            try {
                setErro(null);
                setCarregando(true);

                const res = await api.get(`/api/tipos_culturais/${id}`);
                setTipoCultural(tipoCulturalParaForm(res.data));
            }
            catch (error) {
                setErro(mensagemDeErro(error));
            }
            finally {
                setCarregando(false);
            }
        }

        carregarTipoCultural();
    }, [id])

    async function atualizar(dados) {
        const res = await api.put(`/api/tipos_culturais/${id}`, dados);

        navigate("/admin/tipos-culturais", {state: {mensagem: res.data.mensagem, classe: res.data.classe}});
    }

    function tipoCulturalParaForm(tipoCultural) {
        return {
            nome: tipoCultural.nome,
        }
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Editar Tipo Cultural" />

                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {/* o form só aparece depois de carregar: o useState dele lê o valorInicial uma única vez */}
                {tipoCultural && <TipoCulturalForm valorInicial={tipoCultural} textoBotao="Salvar Alterações" onSalvar={atualizar} />}
            </div>
        </>
    )
}

export default TipoCulturalAtualizar;
