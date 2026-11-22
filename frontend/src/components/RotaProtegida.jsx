import { useEffect, useState } from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { api } from "../services/api";

// Mesmas regras do protegerRota do sistema atual:
//   ["visitante"]               só quem NÃO está logado (logado é mandado para a Home)
//   ["logado"]                  qualquer usuário logado
//   ["user"], ["admin", ...]    só esses perfis (outro perfil vai para /erro)
// Sem login -> /login (aviso), sessão expirada -> /login (aviso).
function RotaProtegida({permissoes}) {
    const location = useLocation();
    const [resultado, setResultado] = useState(null); // null = verificando

    const chave = permissoes.join(",");

    useEffect(() => {
        let ativo = true;

        async function verificar() {
            const apenasVisitante = permissoes.includes("visitante");
            const token = localStorage.getItem("token");

            let novo;

            if(!token) {
                novo = apenasVisitante
                    ? {liberado: true}
                    : {ir: "/login", state: {mensagem: "Você precisa estar logado para acessar essa página.", classe: "warning"}};
            } else {
                try {
                    const res = await api.get("/api/usuarios/me");
                    const usuario = res.data;

                    if(apenasVisitante) {
                        novo = {ir: "/"};
                    } else if(permissoes.includes("logado") || permissoes.includes(usuario.tipo_usuario)) {
                        novo = {liberado: true};
                    } else {
                        novo = {ir: "/erro"};
                    }
                } catch (error) {
                    if(error.response) {
                        localStorage.removeItem("token");
                    }

                    novo = apenasVisitante
                        ? {liberado: true}
                        : {ir: "/login", state: {mensagem: error.response ? "Sua sessão expirou. Faça login novamente." : "Não foi possível falar com o servidor.", classe: "warning"}};
                }
            }

            if(ativo) {
                // guarda a rota a que esse resultado pertence (veja a explicação mais abaixo)
                setResultado({...novo, caminho: location.pathname});
            }
        }

        setResultado(null);
        verificar();

        return () => { ativo = false; };
    }, [chave, location.pathname])

    // O React reaproveita esta mesma instância ao trocar de uma rota protegida para outra
    // (ex.: /favoritos -> /login), então o "resultado" da rota anterior ainda estaria no state
    // por uma renderização. Sem esta checagem ele renderizava o <Navigate> antigo de novo
    // (o toast aparecia duas vezes) e podia exibir por um instante a página de outro grupo
    // (ex.: o painel admin para quem não é admin). Só vale o resultado da rota atual.
    if(!resultado || resultado.caminho != location.pathname) {
        return (<><p className="text-muted">Carregando...</p></>);
    }

    if(resultado.ir) {
        return (<><Navigate to={resultado.ir} replace state={resultado.state} /></>);
    }

    return (<><Outlet /></>);
}

export default RotaProtegida;
