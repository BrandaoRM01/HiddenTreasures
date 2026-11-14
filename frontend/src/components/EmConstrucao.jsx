import Secao from "./Secao";

// Placeholder das rotas que já existem mas cuja página ainda não foi construída.
// Quando o módulo for construído, basta trocar o element da rota no App.jsx.
function EmConstrucao({titulo}) {
    return (
        <>
            <Secao titulo={titulo}>
                <p className="text-muted">Página em construção.</p>
            </Secao>
        </>
    )
}

export default EmConstrucao;
