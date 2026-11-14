import { useEffect, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { api, mensagemDeErro, urlEstatico } from "../../services/api";
import Alerta from "../../components/Alerta";
import CampoSenha from "../../components/CampoSenha";

const FORM_VAZIO = {
    username: "",
    email: "",
    senha: "",
    confirmar_senha: "",
}

function CadastroPagina() {
    const navigate = useNavigate();

    const [form, setForm] = useState(FORM_VAZIO);
    const [foto, setFoto] = useState(null);
    const [preview, setPreview] = useState(null);
    const [erro, setErro] = useState(null);
    const [carregando, setCarregando] = useState(false);

    // preview da foto escolhida (e libera a URL temporária quando troca/sai da página)
    useEffect(() => {
        if(!foto) {
            setPreview(null);
            return;
        }

        const url = URL.createObjectURL(foto);
        setPreview(url);

        return () => URL.revokeObjectURL(url);
    }, [foto])

    function alterarCampo(e) {
        const {name, value} = e.target;
        setForm({...form, [name]: value});
    }

    async function cadastrar(e) {
        e.preventDefault();

        // o backend lê request.form + request.files, então vai como FormData
        // (o axios coloca o Content-Type multipart sozinho)
        const dados = new FormData();
        Object.entries(form).forEach(([chave, valor]) => dados.append(chave, valor));

        if(foto) {
            dados.append("foto", foto);
        }

        try {
            setErro(null);
            setCarregando(true);

            const res = await api.post("/api/usuarios", dados);

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
                <div className="col-md-8 col-lg-7">
                    <div className="card shadow p-4">
                        <h3 className="text-center mb-4">Cadastro</h3>

                        <Alerta mensagem={erro} />

                        <form onSubmit={cadastrar}>
                            <div className="row align-items-start mb-3">
                                <div className="col-md-4 text-center mb-3 mb-md-0">
                                    <label htmlFor="foto" style={{cursor: "pointer"}}>
                                        <img src={preview ?? urlEstatico("img/default/user_foto.webp")} alt="Foto de perfil"
                                            className="rounded-circle shadow"
                                            style={{width: 100, height: 100, objectFit: "cover", objectPosition: "top"}} />
                                    </label>

                                    <input id="foto" type="file" hidden accept="image/*"
                                        onChange={(e) => setFoto(e.target.files[0] ?? null)} />

                                    <label className="btn btn-outline-primary btn-sm mt-2" htmlFor="foto">
                                        <i className="bi bi-upload"></i> Carregar foto
                                    </label>
                                </div>

                                <div className="col-md-8">
                                    <div className="mb-3">
                                        <label className="form-label" htmlFor="username">Username <span className="text-danger">*</span></label>
                                        <input id="username" name="username" type="text" className="form-control" autoComplete="username"
                                            value={form.username} onChange={alterarCampo} />
                                    </div>

                                    <div className="mb-3">
                                        <label className="form-label" htmlFor="email">Email <span className="text-danger">*</span></label>
                                        <input id="email" name="email" type="email" className="form-control" autoComplete="email"
                                            value={form.email} onChange={alterarCampo} />
                                    </div>
                                </div>
                            </div>

                            <div className="row">
                                <div className="col-md-6">
                                    <CampoSenha id="senha" name="senha" rotulo="Senha" autoComplete="new-password"
                                        valor={form.senha} onChange={alterarCampo} />
                                </div>

                                <div className="col-md-6">
                                    <CampoSenha id="confirmar_senha" name="confirmar_senha" rotulo="Confirmar senha" autoComplete="new-password"
                                        valor={form.confirmar_senha} onChange={alterarCampo} />
                                </div>
                            </div>

                            <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                                {carregando ? "Cadastrando..." : "Cadastrar"}
                            </button>
                        </form>

                        <p className="text-center mt-3 mb-0">
                            Já tem conta? <NavLink to="/login">Entrar</NavLink>
                        </p>
                    </div>
                </div>
            </div>
        </>
    )
}

export default CadastroPagina;
