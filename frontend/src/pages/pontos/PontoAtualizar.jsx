import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import PontoForm, { pontoParaForm } from "../../components/PontoForm";
import Alerta from "../../components/Alerta";

// Edição de ponto (admin). A edição de sugestão do usuário reaproveita esta página
// mudando só o título e a rota de volta (veja SugestaoAtualizar.jsx).
function PontoAtualizar({titulo = "Editar Ponto Turístico", rotaVoltar = "/admin/pontos"}) {
    const navigate = useNavigate();

    const { id } = useParams();

    const [ponto, setPonto] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarPonto() {
            try {
                setErro(null);
                setCarregando(true);

                const res = await api.get(`/api/pontos/${id}`);
                setPonto(res.data);
            }
            catch (error) {
                setErro(mensagemDeErro(error));
            }
            finally {
                setCarregando(false);
            }
        }

        carregarPonto();
    }, [id])

    async function atualizar(dados) {
        const res = await api.put(`/api/pontos/${id}`, dados);

        navigate(rotaVoltar, {state: {mensagem: res.data.mensagem, classe: res.data.classe}});
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo={titulo} />

                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {/* o form só aparece depois de carregar: o useState dele lê o valorInicial uma única vez */}
                {ponto && (
                    <PontoForm valorInicial={pontoParaForm(ponto)} imagemInicial={ponto.url_imagem} textoFoto="Trocar foto"
                        textoBotao="Salvar Alterações" rotaVoltar={rotaVoltar} onSalvar={atualizar} />
                )}
            </div>
        </>
    )
}

export default PontoAtualizar;
