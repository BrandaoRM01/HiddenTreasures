import { NavLink } from "react-router-dom";

function LinhaLista({ children, rotaEditar, onExcluir, acoes, py = "py-3" }) {
    return (
        <>
            <div className={`d-flex justify-content-between align-items-center border-bottom ${py}`}>
                {children}

                {acoes !== undefined ? acoes : (
                    <div className="d-flex gap-2">
                        <NavLink to={rotaEditar} className="btn btn-warning btn-sm" title="Editar">
                            <i className="bi bi-pencil"></i>
                        </NavLink>

                        <button type="button" className="btn btn-danger btn-sm d-flex align-items-center justify-content-center"
                            title="Excluir" onClick={onExcluir}>
                            <i className="bi bi-trash"></i>
                        </button>
                    </div>
                )}
            </div>
        </>
    )
}

export default LinhaLista;
