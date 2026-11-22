import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import DestaqueForm from "../../components/DestaqueForm";
import Alerta from "../../components/Alerta";

function DestaqueAtualizar() {
    const navigate = useNavigate();

    const { id } = useParams();

    const [destaque, setDestaque] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarDestaque() {
            try {
                setErro(null);
                setCarregando(true);

                const res = await api.get(`/api/destaques/${id}`);
                setDestaque(destaqueParaForm(res.data));
            }
            catch (error) {
                setErro(mensagemDeErro(error));
            }
            finally {
                setCarregando(false);
            }
        }

        carregarDestaque();
    }, [id])

    async function atualizar(dados) {
        const res = await api.put(`/api/destaques/${id}`, dados);

        navigate("/admin/destaques", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    function destaqueParaForm(destaque) {
        return {
            nome: destaque.nome,
        }
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Editar Destaque" />

                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {destaque && <DestaqueForm valorInicial={destaque} textoBotao="Salvar Alterações" onSalvar={atualizar} />}
            </div>
        </>
    )
}

export default DestaqueAtualizar;
