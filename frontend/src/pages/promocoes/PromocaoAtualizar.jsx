import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import PromocaoForm from "../../components/PromocaoForm";
import Alerta from "../../components/Alerta";

function PromocaoAtualizar() {
    const navigate = useNavigate();

    const { id } = useParams();

    const [promocao, setPromocao] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarPromocao() {
            try {
                setErro(null);
                setCarregando(true);

                const res = await api.get(`/api/promocoes/${id}`);
                setPromocao(promocaoParaForm(res.data));
            }
            catch (error) {
                setErro(mensagemDeErro(error));
            }
            finally {
                setCarregando(false);
            }
        }

        carregarPromocao();
    }, [id])

    async function atualizar(dados) {
        const res = await api.put(`/api/promocoes/${id}`, dados);

        navigate("/admin/promocoes", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    function promocaoParaForm(promocao) {
        return {
            titulo: promocao.titulo,
            descricao: promocao.descricao ?? '',
            desconto: String(promocao.desconto ?? ''),
            data_inicio: promocao.data_inicio,
            data_fim: promocao.data_fim,
        }
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo="Editar Promoção" />

                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {promocao && <PromocaoForm valorInicial={promocao} textoBotao="Salvar Alterações" onSalvar={atualizar} />}
            </div>
        </>
    )
}

export default PromocaoAtualizar;
