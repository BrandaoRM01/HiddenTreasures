import TituloAdmin from "./TituloAdmin";
import Alerta from "./Alerta";

// Esqueleto das páginas "Gerenciar ..." do admin:
//   título -> botão de novo (direita) -> filtro -> erro -> card com a lista -> rodapé (paginação)
// Se children for vazio (null/false) o card da lista não é desenhado.
function LayoutLista({titulo, subtitulo, acao, filtro, erro, classeCard = "p-4", rodape, children}) {
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
