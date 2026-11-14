import { useState } from "react";
import { NavLink, useNavigate, useParams } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import Alerta from "../../components/Alerta";
import CampoSenha from "../../components/CampoSenha";

function RedefinirSenhaPagina() {
    const navigate = useNavigate();

    // vem da rota /redefinir-senha/:token (é o link que chega no email)
    const { token } = useParams();

    const [form, setForm] = useState({senha: "", confirmar_senha: ""});
    const [erro, setErro] = useState(null);
    const [carregando, setCarregando] = useState(false);

    function alterarCampo(e) {
        const {name, value} = e.target;
        setForm({...form, [name]: value});
    }

    async function redefinir(e) {
        e.preventDefault();

        try {
            setErro(null);
            setCarregando(true);

            const res = await api.post(`/api/redefinir-senha/${token}`, form);

            navigate("/login", {state: {mensagem: res.data.mensagem, classe: res.data.classe}});
        } catch (error) {
            setErro(mensagemDeErro(error));
        } finally {
            setCarregando(false);
        }
    }

    return (
        <>
            <div className="row justify-content-center">
                <div className="col-md-6 col-lg-4">
                    <div className="card shadow p-4">
                        <h3 className="text-center mb-3">Redefinir Senha</h3>

                        <Alerta mensagem={erro} />

                        <form onSubmit={redefinir}>
                            <CampoSenha id="senha" name="senha" rotulo="Nova senha" autoComplete="new-password"
                                valor={form.senha} onChange={alterarCampo} />

                            <CampoSenha id="confirmar_senha" name="confirmar_senha" rotulo="Confirmar senha" autoComplete="new-password"
                                valor={form.confirmar_senha} onChange={alterarCampo} />

                            <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                                {carregando ? "Alterando..." : "Alterar senha"}
                            </button>
                        </form>

                        <p className="text-center mt-3 mb-0">
                            <NavLink to="/login">Voltar ao login</NavLink>
                        </p>
                    </div>
                </div>
            </div>
        </>
    )
}

export default RedefinirSenhaPagina;
