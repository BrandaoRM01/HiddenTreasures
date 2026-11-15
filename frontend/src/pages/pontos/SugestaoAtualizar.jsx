import PontoAtualizar from "./PontoAtualizar";

// Mesma tela de edição do ponto, só que para o usuário comum editar a própria sugestão.
function SugestaoAtualizar() {
    return (
        <>
            <PontoAtualizar titulo="Editar Sugestão de Ponto Turístico" rotaVoltar="/sugerir-ponto" />
        </>
    )
}

export default SugestaoAtualizar;
