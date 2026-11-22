import Secao from "./Secao";

function EmConstrucao({ titulo }) {
    return (
        <>
            <Secao titulo={titulo}>
                <p className="text-muted">Página em construção.</p>
            </Secao>
        </>
    )
}

export default EmConstrucao;
