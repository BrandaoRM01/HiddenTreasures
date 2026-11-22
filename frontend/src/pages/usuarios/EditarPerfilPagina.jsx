import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, mensagemDeErro, urlEstatico } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import Alerta from "../../components/Alerta";
import CampoSenha from "../../components/CampoSenha";

function EditarPerfilPagina() {
    const navigate = useNavigate();

    const [usuario, setUsuario] = useState(null);
    const [form, setForm] = useState({ username: "", senha: "", confirmar_senha: "" });
    const [foto, setFoto] = useState(null);
    const [preview, setPreview] = useState(null);
    const [carregando, setCarregando] = useState(false);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarPerfil() {
            try {
                setErro(null);

                const res = await api.get("/api/usuarios/me");

                setUsuario(res.data);
                setForm(atual => ({ ...atual, username: res.data.username }));
            } catch (error) {
                setErro(mensagemDeErro(error));
            }
        }
        carregarPerfil();
    }, [])

    useEffect(() => {
        if (!foto) {
            setPreview(null);
            return;
        }

        const url = URL.createObjectURL(foto);
        setPreview(url);

        return () => URL.revokeObjectURL(url);
    }, [foto])

    function alterarCampo(e) {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    }

    async function salvar(e) {
        e.preventDefault();

        const dados = new FormData();
        Object.entries(form).forEach(([chave, valor]) => dados.append(chave, valor));

        if (foto) {
            dados.append("foto", foto);
        }

        try {
            setCarregando(true);

            const res = await api.put("/api/usuarios/me", dados);

            navigate("/", { state: { mensagem: res.data.mensagem, classe: res.data.classe } });
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        } finally {
            setCarregando(false);
        }
    }

    return (
        <>
            <div className="row justify-content-center">
                <div className="col-md-8 col-lg-6">
                    <div className="card shadow p-4">

                        <h3 className="text-center mb-3">Editar Perfil</h3>

                        <Alerta mensagem={erro} />

                        {usuario && (
                            <>
                                <div className="text-center mb-4">
                                    <p className="text-muted mb-1 small">Conta vinculada</p>
                                    <p className="fw-semibold mb-0">
                                        <i className="bi bi-envelope me-1"></i>
                                        <span>{usuario.email}</span>
                                    </p>
                                </div>

                                <form onSubmit={salvar}>

                                    <div className="text-center mb-4">
                                        <label htmlFor="foto-imagem" style={{ cursor: "pointer" }}>
                                            <img src={preview ?? urlEstatico(usuario.url_foto)} alt="Foto de perfil" className="rounded-circle shadow"
                                                style={{ width: "110px", height: "110px", objectFit: "cover", objectPosition: "top" }} />
                                        </label>

                                        <input name="foto" type="file" hidden id="foto-imagem" accept="image/*"
                                            onChange={(e) => setFoto(e.target.files[0] ?? null)} />

                                        <div className="mt-2">
                                            <label className="btn btn-outline-primary btn-sm me-2" htmlFor="foto-imagem">
                                                <i className="bi bi-upload"></i> Trocar foto
                                            </label>
                                        </div>
                                    </div>

                                    <div className="mb-4">
                                        <label htmlFor="username" className="form-label fw-semibold">Username <span className="text-danger">*</span></label>
                                        <input id="username" name="username" type="text" className="form-control" autoComplete="username"
                                            value={form.username} onChange={alterarCampo} />
                                    </div>

                                    <div className="row">
                                        <div className="col-md-6">
                                            <CampoSenha id="perfil_senha" name="senha" rotulo="Nova senha" obrigatorio={false} autoComplete="new-password"
                                                valor={form.senha} onChange={alterarCampo} />
                                        </div>

                                        <div className="col-md-6">
                                            <CampoSenha id="perfil_confirmar_senha" name="confirmar_senha" rotulo="Confirmar senha" obrigatorio={false} autoComplete="new-password"
                                                valor={form.confirmar_senha} onChange={alterarCampo} />
                                        </div>
                                    </div>

                                    <button type="submit" className="btn btn-primary w-100 mt-2" disabled={carregando}>
                                        {carregando ? "Salvando..." : "Salvar Alterações"}
                                    </button>

                                </form>
                            </>
                        )}

                    </div>
                </div>
            </div>
        </>
    )
}

export default EditarPerfilPagina;
