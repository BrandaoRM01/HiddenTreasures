import { useEffect, useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { api, mensagemDeErro, urlEstatico } from "../services/api";

function NavBar() {
    const navigate = useNavigate();
    const location = useLocation();

    // undefined = ainda carregando, null = visitante, objeto = usuário logado
    const [usuario, setUsuario] = useState(undefined);
    const [menuAberto, setMenuAberto] = useState(false);
    const [dropdownAberto, setDropdownAberto] = useState(false);

    // Igual ao nav.js do sistema atual: a cada página, confere o token em /api/usuarios/me
    useEffect(() => {
        let ativo = true;

        async function carregarUsuario() {
            if(!localStorage.getItem("token")) {
                setUsuario(null);
                return;
            }

            try {
                const res = await api.get("/api/usuarios/me");

                if(ativo) {
                    setUsuario(res.data);
                }
            } catch (error) {
                if(error.response) {
                    localStorage.removeItem("token");
                }

                if(ativo) {
                    setUsuario(null);
                }
            }
        }

        carregarUsuario();
        setMenuAberto(false);
        setDropdownAberto(false);

        return () => { ativo = false; };
    }, [location.pathname])

    const logado = Boolean(usuario);
    const ehModerador = logado && (usuario.tipo_usuario == "admin" || usuario.tipo_usuario == "superadmin");

    async function sair(e) {
        e.preventDefault();

        try {
            await api.post("/logout");
        } catch (error) {
            // o logout no sistema é só limpar o token; se a API falhar, sai do mesmo jeito
        }

        localStorage.removeItem("token");
        setUsuario(null);
        navigate("/");
    }

    async function excluirPerfil(e) {
        e.preventDefault();

        if(!window.confirm("Tem certeza que deseja excluir seu perfil?")) {
            return;
        }

        try {
            await api.delete("/api/usuarios/me");

            localStorage.removeItem("token");
            setUsuario(null);
            navigate("/");
        } catch (error) {
            window.alert(mensagemDeErro(error));
        }
    }

    return (
        <>
            <nav className="navbar navbar-expand-lg navbar-light bg-white shadow-sm fixed-top">
                <div className="container">
                    <NavLink className="navbar-brand fw-bold" to="/">HiddenTreasures</NavLink>

                    <button className="navbar-toggler" type="button" onClick={() => setMenuAberto(!menuAberto)}>
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    <div className={`collapse navbar-collapse ${menuAberto ? "show" : ""}`}>
                        <ul className="navbar-nav me-auto">
                            <li className="nav-item">
                                <NavLink className="nav-link" to="/" end>Home</NavLink>
                            </li>

                            <li className="nav-item">
                                <NavLink className="nav-link" to="/pontos">Pontos Turísticos</NavLink>
                            </li>

                            {logado && !ehModerador && (
                                <li className="nav-item">
                                    <NavLink className="nav-link" to="/sugerir-ponto">Sugerir Ponto</NavLink>
                                </li>
                            )}

                            {logado && (
                                <li className="nav-item">
                                    <NavLink className="nav-link" to="/favoritos">Favoritos</NavLink>
                                </li>
                            )}

                            <li className="nav-item">
                                <NavLink className="nav-link" to="/sobre">Sobre</NavLink>
                            </li>

                            {ehModerador && (
                                <li className="nav-item">
                                    <NavLink className="nav-link text-warning fw-semibold" to="/admin/painel-admin">Painel Admin</NavLink>
                                </li>
                            )}
                        </ul>

                        {usuario === null && (
                            <div className="d-flex gap-2">
                                <NavLink to="/login" className="btn btn-outline-primary">Login</NavLink>
                                <NavLink to="/cadastro" className="btn btn-primary">Cadastrar</NavLink>
                            </div>
                        )}

                        {logado && (
                            <div className="dropdown">
                                <a href="#" className="d-flex align-items-center text-decoration-none dropdown-toggle text-dark"
                                    onClick={(e) => { e.preventDefault(); setDropdownAberto(!dropdownAberto); }}>
                                    <img src={urlEstatico(usuario.url_foto)} alt="Foto de perfil" className="rounded-circle"
                                        width="38" height="38" style={{objectFit: "cover"}} />
                                    <span className="ms-2">{usuario.username}</span>
                                </a>

                                <ul className={`dropdown-menu dropdown-menu-end ${dropdownAberto ? "show" : ""}`}>
                                    <li><a className="dropdown-item" href="#" onClick={sair}>Logout</a></li>
                                    <li><NavLink className="dropdown-item" to="/editar-perfil">Editar Perfil</NavLink></li>
                                    {usuario.tipo_usuario != "superadmin" && (
                                        <li>
                                            <a className="dropdown-item text-danger" href="#" onClick={excluirPerfil}>Excluir Perfil</a>
                                        </li>
                                    )}
                                </ul>
                            </div>
                        )}
                    </div>
                </div>
            </nav>
        </>
    );
}

export default NavBar;
