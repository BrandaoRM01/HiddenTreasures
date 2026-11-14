import { NavLink } from "react-router-dom";

// Estado "nenhum registro" das listas simples (ícone, título, texto e botão de criar).
function ListaVazia({icone, titulo, texto, rota, textoBotao}) {
    return (
        <>
            <div className="text-center py-5">
                <div className="mb-3">
                    <i className={`bi ${icone}`} style={{fontSize: "50px", color: "#6c757d"}}></i>
                </div>

                <h4 className="mb-2">{titulo}</h4>
                <p className="text-muted">{texto}</p>

                <NavLink to={rota} className="btn btn-primary mt-3">{textoBotao}</NavLink>
            </div>
        </>
    )
}

export default ListaVazia;
