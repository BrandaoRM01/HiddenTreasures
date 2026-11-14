function Filtro({ busca, onBuscaChange, placeholder = "Buscar por nome" }) {
    return (
        <>
            <div className="p-3 mb-4">
                <div className="row g-3">
                    <div className="col-md-3">
                        <input className="form-control" type="text"
                            placeholder={placeholder}
                            value={busca}
                            onChange={(e) => onBuscaChange(e.target.value)} />
                    </div>
                </div>
            </div>
        </>
    )
}

export default Filtro;
