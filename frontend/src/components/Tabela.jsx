import { NavLink } from "react-router-dom";

function Tabela({ colunas, itens, rotaEditar, onDelete, vazio = "Nenhum registro encontrado." }) {
    if (itens.length == 0) {
        return (<><p className="text-muted">{vazio}</p></>);
    }

    return (
        <>
            <div className="table-responsive">
                <table className="table table-striped table-hover bg-white shadow-sm align-middle">
                    <thead className="table-dark">
                        <tr>
                            {colunas.map(coluna => (
                                <th key={coluna.titulo}>{coluna.titulo}</th>
                            ))}
                            {rotaEditar && <th></th>}
                            {onDelete && <th></th>}
                        </tr>
                    </thead>
                    <tbody>
                        {
                            itens.map(item => {
                                const rota = rotaEditar ? rotaEditar(item) : null;

                                return (
                                    <tr key={item.id ?? item.email}>
                                        {colunas.map(coluna => (
                                            <td key={coluna.titulo}>{coluna.render ? coluna.render(item) : item[coluna.campo]}</td>
                                        ))}
                                        {rotaEditar && <td>{rota && <NavLink className="btn btn-warning" to={rota}>Editar</NavLink>}</td>}
                                        {onDelete && <td><button onClick={() => onDelete(item)} className="btn btn-danger">Excluir</button></td>}
                                    </tr>
                                );
                            })
                        }
                    </tbody>
                </table>
            </div>
        </>
    )
}

export default Tabela;
