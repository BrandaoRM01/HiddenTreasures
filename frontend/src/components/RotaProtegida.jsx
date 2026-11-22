import { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { api } from "../services/api";

function RotaProtegida({ permissoes }) {
    const location = useLocation();
    const [resultado, setResultado] = useState(null);

    const chave = permissoes.join(",");

    useEffect(() => {
        let ativo = true;

        async function verificar() {
            const apenasVisitante = permissoes.includes("visitante");
            const token = localStorage.getItem("token");

            let novo;

            if (!token) {
                novo = apenasVisitante
                    ? { liberado: true }
                    : { ir: "/login", state: { mensagem: "Você precisa estar logado para acessar essa página.", classe: "warning" } };
            } else {
                try {
                    const res = await api.get("/api/usuarios/me");
                    const usuario = res.data;

                    if (apenasVisitante) {
                        novo = { ir: "/" };
                    } else if (permissoes.includes("logado") || permissoes.includes(usuario.tipo_usuario)) {
                        novo = { liberado: true };
                    } else {
                        novo = { ir: "/erro" };
                    }
                } catch (error) {
                    if (error.response) {
                        localStorage.removeItem("token");
                    }

                    novo = apenasVisitante
                        ? { liberado: true }
                        : { ir: "/login", state: { mensagem: error.response ? "Sua sessão expirou. Faça login novamente." : "Não foi possível falar com o servidor.", classe: "warning" } };
                }
            }

            if (ativo) {
                setResultado({ ...novo, caminho: location.pathname });
            }
        }

        setResultado(null);
        verificar();

        return () => { ativo = false; };
    }, [chave, location.pathname])

    if (!resultado || resultado.caminho != location.pathname) {
        return (<><p className="text-muted">Carregando...</p></>);
    }

    if (resultado.ir) {
        return (<><Navigate to={resultado.ir} replace state={resultado.state} /></>);
    }

    return (<><Outlet /></>);
}

export default RotaProtegida;
