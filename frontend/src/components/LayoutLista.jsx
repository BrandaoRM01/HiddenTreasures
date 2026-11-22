import TituloAdmin from "./TituloAdmin";
import Alerta from "./Alerta";

function LayoutLista({ titulo, subtitulo, acao, filtro, erro, classeCard = "p-4", rodape, children }) {
    return (
        <>
            <div className="mt-4">
                <TituloAdmin titulo={titulo} subtitulo={subtitulo} />

                {acao && <div className="d-flex justify-content-end mb-3">{acao}</div>}

                {filtro}

                <Alerta mensagem={erro} />

                {children && <div className={`card ${classeCard} shadow`}>{children}</div>}

                {rodape}
            </div>
        </>
    )
}

export default LayoutLista;
