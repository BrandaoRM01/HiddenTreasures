function Alerta({mensagem, classe = "danger"}) {
    if(!mensagem) {
        return null;
    }

    return (
        <>
            <div className={`alert alert-${classe}`} role="alert">
                {mensagem}
            </div>
        </>
    )
}

export default Alerta;
