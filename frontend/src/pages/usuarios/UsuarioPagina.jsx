import { useState, useEffect } from "react";
import { api, mensagemDeErro, urlEstatico } from "../../services/api";
import { mostrarMensagem } from "../../services/mensagem";
import LayoutLista from "../../components/LayoutLista";
import Filtro from "../../components/Filtro";
import LinhaLista from "../../components/LinhaLista";

function UsuarioPagina() {
    const [busca, setBusca] = useState("");
    const [usuarios, setUsuarios] = useState([]);
    const [usuarioLogado, setUsuarioLogado] = useState(null);
    const [carregando, setCarregando] = useState(true);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarUsuarios() {
            try {
                setErro(null);
                const res = await api.get("/api/usuarios");
                setUsuarios(res.data.usuarios);
                setUsuarioLogado(res.data.usuario_logado);
            } catch (error) {
                setErro(mensagemDeErro(error));
            } finally {
                setCarregando(false);
            }
        }
        carregarUsuarios();
    }, [])

    let listaFiltrada = usuarios.filter(u =>
        u.username.toLowerCase().includes(busca.toLowerCase()) ||
        u.email.toLowerCase().includes(busca.toLowerCase())
    );

    async function alterarPermissao(usuario) {
        let novoTipo = usuario.tipo_usuario == "admin" ? "user" : "admin";

        // o backend lê o tipo pelo request.form, então vai como FormData
        let dados = new FormData();
        dados.append("tipo_usuario", novoTipo);

        try {
            const res = await api.put(`/api/usuarios/${usuario.email}`, dados);

            setUsuarios(usuarios.map(u => u.email == usuario.email ? {...u, tipo_usuario: novoTipo} : u));
            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    async function excluir(usuario) {
        if(!window.confirm(`Tem certeza que deseja excluir o usuário ${usuario.username}?`)) {
            return;
        }

        try {
            const res = await api.delete(`/api/usuarios/${usuario.email}`);

            setUsuarios(usuarios.filter(u => u.email != usuario.email));
            mostrarMensagem(res.data.mensagem, res.data.classe);
        } catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
    }

    // só o superadmin gerencia, e nunca outro superadmin
    function acoesDoUsuario(usuario) {
        let podeGerenciar = usuarioLogado?.tipo_usuario == "superadmin" && usuario.tipo_usuario != "superadmin";

        if(!podeGerenciar) {
            return null;
        }

        return (
            <div className="d-flex gap-2">
                <button type="button" onClick={() => alterarPermissao(usuario)}
                    className={usuario.tipo_usuario == "admin" ? "btn btn-secondary btn-sm flex-fill" : "btn btn-warning btn-sm flex-fill"}>
                    {usuario.tipo_usuario == "admin" ? "Remover Admin" : "Tornar Admin"}
                </button>

                <button type="button" className="btn btn-danger flex-fill" title="Excluir" onClick={() => excluir(usuario)}>
                    <i className="bi bi-trash"></i>
                </button>
            </div>
        );
    }

    function renderizarLista() {
        if(carregando) {
            return (<p className="text-muted mb-0">Carregando...</p>);
        }

        if(erro) {
            return null;
        }

        if(listaFiltrada.length == 0) {
            return (<p className="text-muted text-center py-4 mb-0">Nenhum usuário encontrado.</p>);
        }

        return listaFiltrada.map(usuario => (
            <LinhaLista key={usuario.email} py="py-2" acoes={acoesDoUsuario(usuario)}>
                <div className="d-flex align-items-center">
                    <img src={urlEstatico(usuario.url_foto)} alt={usuario.username} width="40" height="40"
                        style={{objectFit: "cover"}} className="rounded-circle me-2" />

                    <div>
                        <strong>{usuario.username}</strong><br />
                        <small>{usuario.email}</small><br />
                        <span className="badge bg-secondary">{usuario.tipo_usuario}</span>
                    </div>
                </div>
            </LinhaLista>
        ));
    }

    return (
        <>
            <LayoutLista
                titulo="Gerenciar Usuários"
                classeCard="p-3"
                erro={erro}
                filtro={usuarios.length > 0 && <Filtro busca={busca} onBuscaChange={setBusca} placeholder="Buscar por usuário ou email" />}
            >
                {renderizarLista()}
            </LayoutLista>
        </>
    )
}

export default UsuarioPagina;
