import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import Alerta from "../../components/Alerta";
import CampoSenha from "../../components/CampoSenha";

function LoginPagina() {
    const navigate = useNavigate();

    const [form, setForm] = useState({email: "", senha: ""});
    const [erro, setErro] = useState(null);
    const [carregando, setCarregando] = useState(false);

    function alterarCampo(e) {
        const {name, value} = e.target;
        setForm({...form, [name]: value});
    }

    async function entrar(e) {
        e.preventDefault();

        try {
            setErro(null);
            setCarregando(true);

            const res = await api.post("/api/usuarios/auth", form);

            localStorage.setItem("token", res.data.token);
            navigate("/", {state: {mensagem: res.data.mensagem, classe: res.data.classe}});
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
                        <h3 className="text-center mb-4">Login</h3>

                        <Alerta mensagem={erro} />

                        <form onSubmit={entrar}>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="email">Email <span className="text-danger">*</span></label>
                                <input id="email" name="email" type="email" className="form-control" autoComplete="email"
                                    value={form.email} onChange={alterarCampo} />
                            </div>

                            <CampoSenha id="senha" name="senha" rotulo="Senha" autoComplete="current-password"
                                valor={form.senha} onChange={alterarCampo} />

                            <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                                {carregando ? "Entrando..." : "Entrar"}
                            </button>
                        </form>

                        <div className="text-center mt-2">
                            <NavLink to="/recuperar-senha" className="text-decoration-none">Esqueceu a senha?</NavLink>
                        </div>

                        <p className="text-center mt-3 mb-0">
                            Não tem conta? <NavLink to="/cadastro">Cadastre-se</NavLink>
                        </p>
                    </div>
                </div>
            </div>
        </>
    )
}

export default LoginPagina;
