import { NavLink } from "react-router-dom";

const MODULOS = [
    {titulo: "Categorias", descricao: "Gerencie as categorias dos pontos turísticos", rota: "/admin/categorias"},
    {titulo: "Pontos Turísticos", descricao: "Adicione ou edite destinos", rota: "/admin/pontos"},
    {titulo: "Promoções", descricao: "Crie e gerencie descontos para os pontos turísticos", rota: "/admin/promocoes"},
    {titulo: "Usuários", descricao: "Gerencie os usuários do sistema", rota: "/admin/usuarios"},
    {titulo: "Ecossistemas", descricao: "Gerencie os ecossistemas dos pontos naturais", rota: "/admin/ecossistemas"},
    {titulo: "Tipos Culturais", descricao: "Gerencie os tipos dos pontos culturais", rota: "/admin/tipos-culturais"},
    {titulo: "Destaques", descricao: "Gerencie os destaques disponíveis para os pontos turísticos", rota: "/admin/destaques"},
    {titulo: "Sugestões", descricao: "Visualize e modere as sugestões enviadas pelos usuários", rota: "/admin/sugestoes"},
];

function PainelAdminPagina() {
    return (
        <>
            <div className="text-center mb-5">
                <h1 className="fw-bold">Painel Administrativo</h1>
            </div>

            <div className="row justify-content-center align-items-stretch">
                {MODULOS.map(modulo => (
                    <div className="col-md-4 mb-4 d-flex" key={modulo.rota}>
                        <div className="card shadow text-center p-4 card-hover h-100 w-100 d-flex flex-column">
                            <h3 className="fw-bold">{modulo.titulo}</h3>
                            <p>{modulo.descricao}</p>
                            <NavLink to={modulo.rota} className="btn btn-primary mt-auto">Acessar</NavLink>
                        </div>
                    </div>
                ))}
            </div>
        </>
    )
}

export default PainelAdminPagina;
