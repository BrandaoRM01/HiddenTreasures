function Paginacao({ paginacao, onMudar }) {
    if (!paginacao || paginacao.total_paginas <= 1) {
        return null;
    }

    const paginas = Array.from({ length: paginacao.total_paginas }, (_, i) => i + 1);

    return (
        <>
            <nav className="mt-4">
                <ul className="pagination justify-content-center">
                    {
                        paginas.map(pagina => (
                            <li key={pagina} className={`page-item ${pagina == paginacao.page ? "active" : ""}`}>
                                <button type="button" className="page-link" onClick={() => onMudar(pagina)}>{pagina}</button>
                            </li>
                        ))
                    }
                </ul>
            </nav>
        </>
    )
}

export default Paginacao;
