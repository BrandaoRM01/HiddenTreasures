import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import TituloAdmin from "../../components/TituloAdmin";
import PontoForm, { pontoParaForm } from "../../components/PontoForm";
import Alerta from "../../components/Alerta";

function PontoAtualizar({ titulo = "Editar Ponto Turístico", rotaVoltar = "/admin/pontos" }) {
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

        navigate(rotaVoltar, { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
    }

    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo={titulo} />

                <Alerta mensagem={erro} />

                {carregando && <p className="text-muted">Carregando...</p>}

                {ponto && (
                    <PontoForm valorInicial={pontoParaForm(ponto)} imagemInicial={ponto.url_imagem} textoFoto="Trocar foto"
                        textoBotao="Salvar Alterações" rotaVoltar={rotaVoltar} onSalvar={atualizar} />
                )}
            </div>
        </>
    )
}

export default PontoAtualizar;
