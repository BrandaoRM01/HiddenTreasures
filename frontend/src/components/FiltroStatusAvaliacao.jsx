import Dropdown from "./Dropdown";

const OPCOES = [
    {texto: "Todas", valor: ""},
    {texto: "Aprovadas", valor: "aprovado"},
    {texto: "Pendentes", valor: "pendente"},
    {texto: "Rejeitadas", valor: "rejeitado"},
];

// Dropdown de filtro por status das avaliações (só aparece para admin) — criarDropdownFiltroStatus do main.js
function FiltroStatusAvaliacao({filtro, onSelecionar}) {
    const atual = OPCOES.find(opcao => opcao.valor === filtro) || OPCOES[0];

    return (
        <>
            <Dropdown classeBotao="btn btn-outline-secondary btn-sm dropdown-toggle" rotuloBotao={atual.texto}
                itens={OPCOES.map(opcao => ({texto: opcao.texto, onClick: () => onSelecionar(opcao.valor)}))} />
        </>
    )
}

export default FiltroStatusAvaliacao;
