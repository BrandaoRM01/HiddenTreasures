import { NavLink } from "react-router-dom";

function PaginaErro({mensagem = "Você não tem permissão para acessar essa página."}) {
    return (
        <>
            <div className="text-center mt-5">
                <h1 className="display-4 text-danger">Erro</h1>
                <p className="lead">{mensagem}</p>
                <NavLink className="btn btn-primary" to="/">Voltar para Home</NavLink>
            </div>
        </>
    )
}

export default PaginaErro;
