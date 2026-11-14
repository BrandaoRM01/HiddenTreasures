function Secao({titulo, acoes, children}) {
    return (
        <>
        <section className="my-5">
            <div className="d-flex justify-content-between align-items-center mb-3">
                <h3>{titulo}</h3>
                {acoes}
            </div>
            {children}
        </section>
        </>
    )
}

export default Secao;
