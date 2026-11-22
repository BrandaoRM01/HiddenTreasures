function TituloAdmin({ titulo, subtitulo }) {
    return (
        <>
            <div className="text-center mb-5">
                <h1 className="fw-bold">{titulo}</h1>
                {subtitulo && <p className="text-muted">{subtitulo}</p>}
            </div>
        </>
    )
}

export default TituloAdmin;
