import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import EcossistemaForm from "../../components/EcossistemaForm";
import Alerta from "../../components/Alerta";

function EcossistemaAtualizar() {
    const navigate = useNavigate();

    const { id } = useParams();

    const [ecossistema, setEcossistema] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarEcossistema() {
            try {
                setErro(null);
                setCarregando(true);

                const res = await api.get(`/api/ecossistemas/${id}`);
                setEcossistema(ecossistemaParaForm(res.data));
            }
            catch (error) {
                setErro(mensagemDeErro(error));
            }
            finally {
                setCarregando(false);
            }
        }

        carregarEcossistema();
    }, [id])

    async function atualizar(dados) {
        const res = await api.put(`/api/ecossistemas/${id}`, dados);

        navigate("/admin/ecossistemas", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    function ecossistemaParaForm(ecossistema) {
        return {
            nome: ecossistema.nome,
        }
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Editar Ecossistema" />

                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {ecossistema && <EcossistemaForm valorInicial={ecossistema} textoBotao="Salvar Alterações" onSalvar={atualizar} />}
            </div>
        </>
    )
}

export default EcossistemaAtualizar;
