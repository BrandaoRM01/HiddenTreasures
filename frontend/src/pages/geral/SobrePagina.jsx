import { urlEstatico } from "../../services/api";

const SOBRE_CARDS = [
    {titulo: "Explorar", texto: "Navegue por uma lista de pontos turísticos organizados por avaliação, categoria e popularidade. Descubra lugares incríveis ao redor do mundo."},
    {titulo: "Avaliar", texto: "Usuários podem avaliar os pontos turísticos com notas e comentários, ajudando outros viajantes a escolher melhores destinos."},
    {titulo: "Salvar favoritos", texto: "Cada usuário pode marcar seus pontos turísticos preferidos, criando uma lista personalizada de lugares para visitar depois."},
];

const RECURSOS = [
    {titulo: "⭐ Sistema de avaliações", texto: "Cada ponto turístico possui uma média de avaliação calculada automaticamente com base nas notas dos usuários."},
    {titulo: "🏷️ Categorias e tipos", texto: "Os pontos são organizados por categorias e tipos culturais ou naturais, facilitando a navegação e descoberta."},
    {titulo: "🔥 Promoções", texto: "Alguns pontos turísticos possuem promoções ativas com desconto no valor de entrada, destacadas na página inicial."},
    {titulo: "📍 Destaques", texto: "Cada local pode conter destaques especiais, como características únicas, experiências ou atrações principais."},
    {titulo: "🧭 Detalhes completos", texto: "Cada ponto possui uma página própria com informações completas, incluindo avaliações, descrição e dados de visita."},
    {titulo: "👤 Sistema de usuários", texto: "O sistema conta com login, favoritos e interações que personalizam a experiência de cada usuário."},
];

function SobrePagina() {
    return (
        <>
            <div className="mt-4">

                <div className="text-center mb-5">
                    <h1 className="fw-bold">Sobre o HiddenTreasures</h1>
                    <p className="text-muted">Descobrindo o que o mundo esconde</p>
                </div>

                <div className="row align-items-center">
                    <div className="col-md-6">
                        <h3><strong>Nosso propósito</strong></h3>

                        <p>
                            O <strong>HiddenTreasures</strong> é uma plataforma desenvolvida para explorar,
                            divulgar e valorizar pontos turísticos ao redor do mundo, desde locais famosos
                            até lugares pouco conhecidos que muitas vezes passam despercebidos.
                        </p>

                        <p>
                            O sistema permite que usuários descubram novos destinos, visualizem informações
                            detalhadas, fotos, localização, custo de entrada, horário de funcionamento
                            e avaliações feitas pela comunidade.
                        </p>

                        <p>
                            Além disso, o projeto também destaca experiências especiais como
                            promoções em pontos turísticos e destaques criados pela comunidade,
                            ajudando a enriquecer a descoberta de novos lugares.
                        </p>
                    </div>

                    <div className="col-md-6">
                        <img src={urlEstatico("img/default/hidden_treasures_logo.png")} alt="Logo do HiddenTreasures"
                            className="img-fluid rounded shadow" />
                    </div>
                </div>

                <div className="row mt-5">
                    {SOBRE_CARDS.map(card => (
                        <div className="col-md-4 text-center" key={card.titulo}>
                            <h4><strong>{card.titulo}</strong></h4>
                            <p>{card.texto}</p>
                        </div>
                    ))}
                </div>

                <hr className="my-5" />

                <div className="text-center mb-4">
                    <h3><strong>Recursos do sistema</strong></h3>
                </div>

                <div className="row">
                    {RECURSOS.map(recurso => (
                        <div className="col-md-6 mb-3" key={recurso.titulo}>
                            <h5>{recurso.titulo}</h5>
                            <p>{recurso.texto}</p>
                        </div>
                    ))}
                </div>

            </div>
        </>
    )
}

export default SobrePagina;
