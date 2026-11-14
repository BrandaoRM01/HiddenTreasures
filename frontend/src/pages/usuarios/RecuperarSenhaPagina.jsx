import { useState } from "react";
import { NavLink } from "react-router-dom";
import { api, mensagemDeErro } from "../../services/api";
import Alerta from "../../components/Alerta";

function RecuperarSenhaPagina() {
    const [email, setEmail] = useState("");
    const [aviso, setAviso] = useState(null); // {mensagem, classe}
    const [carregando, setCarregando] = useState(false);

    async function enviar(e) {
        e.preventDefault();

        try {
            setAviso(null);
            setCarregando(true);

            const res = await api.post("/api/recuperacao-senha", {email});

            setEmail("");
            setAviso({mensagem: res.data.mensagem, classe: res.data.classe});
        } catch (error) {
            setAviso({mensagem: mensagemDeErro(error), classe: "danger"});
        } finally {
            setCarregando(false);
        }
    }

    return (
        <>
            <div className="row justify-content-center">
                <div className="col-md-6 col-lg-4">
                    <div className="card shadow p-4">
                        <h3 className="text-center mb-3">Recuperar Senha</h3>

                        <p className="text-center text-muted">
                            Digite seu email para receber o link de redefinição.
                        </p>

                        <Alerta mensagem={aviso?.mensagem} classe={aviso?.classe} />

                        <form onSubmit={enviar}>
                            <div className="mb-3">
                                <label className="form-label" htmlFor="email">Email <span className="text-danger">*</span></label>
                                <input id="email" name="email" type="email" className="form-control" required autoComplete="email"
                                    value={email} onChange={(e) => setEmail(e.target.value)} />
                            </div>

                            <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                                {carregando ? "Enviando..." : "Enviar link"}
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

export default RecuperarSenhaPagina;
