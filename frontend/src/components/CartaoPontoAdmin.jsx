import { urlEstatico } from "../services/api";
import BadgeStatus from "./BadgeStatus";

function CartaoPontoAdmin({ ponto, detalhes, classeBotoes, classeCartao = "card shadow-sm border-0", children }) {
    const tipoLabel = ponto.tipo_ponto.charAt(0).toUpperCase() + ponto.tipo_ponto.slice(1);

    return (
        <>
            <div className="col-12">
                <div className={classeCartao}>
                    <div className="card-body">
                        <div className="row align-items-center">

                            <div className="col-lg-8">
                                <div className="d-flex align-items-center gap-3">
                                    <img src={urlEstatico(ponto.url_imagem)} alt={ponto.nome} className="rounded shadow-sm"
                                        style={{ width: "100px", height: "100px", objectFit: "cover" }} />

                                    <div>
                                        <h5 className="fw-bold mb-1">{ponto.nome}</h5>
                                        <p className="text-muted mb-1"><i className="bi bi-geo-alt-fill"></i> {ponto.localizacao}</p>
                                        <p className="mb-1"><strong>Categoria:</strong> {ponto.categoria.nome}</p>
                                        <p className="mb-1"><strong>Tipo:</strong> {tipoLabel}</p>
                                        {detalhes}
                                    </div>
                                </div>
                            </div>

                            <div className="col-lg-4 text-lg-end mt-3 mt-lg-0">
                                <BadgeStatus status={ponto.status} className="fs-6 mb-3" />
                                <br />
                                <div className={classeBotoes}>
                                    {children}
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default CartaoPontoAdmin;
