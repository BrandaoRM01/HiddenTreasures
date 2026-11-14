import { useState, useEffect } from "react";
import { api, mensagemDeErro } from "../../services/api";
import CardPonto from "../../components/CardPonto";
import Paginacao from "../../components/Paginacao";
import Alerta from "../../components/Alerta";

const FILTROS_VAZIOS = {busca: "", categoria: "", tipo: "", localizacao: ""};

function PontoPagina() {
    const [form, setForm] = useState(FILTROS_VAZIOS);        // o que está digitado
    const [filtros, setFiltros] = useState(FILTROS_VAZIOS);  // o que foi aplicado (botão Filtrar)
    const [pagina, setPagina] = useState(1);

    const [categorias, setCategorias] = useState([]);
    const [pontos, setPontos] = useState([]);
    const [logado, setLogado] = useState(false);
    const [paginacao, setPaginacao] = useState(null);
    const [erro, setErro] = useState(null);

    useEffect(() => {
        async function carregarCategorias() {
            try {
                const res = await api.get("/api/categorias");
                setCategorias(res.data);
            } catch (error) {
                setErro(mensagemDeErro(error));
            }
        }
        carregarCategorias();
    }, [])

    useEffect(() => {
        async function carregarPontos() {
            try {
                setErro(null);

                const params = {status: "aprovado", page: pagina, limit: 9};
                if(filtros.busca.trim()) params.busca = filtros.busca.trim();
                if(filtros.categoria) params.categoria = filtros.categoria;
                if(filtros.tipo) params.tipo = filtros.tipo;
                if(filtros.localizacao.trim()) params.localizacao = filtros.localizacao.trim();

                const res = await api.get("/api/pontos", {params});

                setPontos(res.data.pontos);
                setLogado(res.data.logado);
                setPaginacao(res.data.paginacao);
            } catch (error) {
                setErro(mensagemDeErro(error));
            }
        }
        carregarPontos();
    }, [filtros, pagina])

    function alterarCampo(e) {
        const {name, value} = e.target;
        setForm({...form, [name]: value});
    }

    function filtrar(e) {
        e.preventDefault();
        setPagina(1);
        setFiltros(form);
    }

    function mudarPagina(novaPagina) {
        setPagina(novaPagina);
        window.scrollTo({top: 0, behavior: "smooth"});
    }

    return (
        <>
            <div className="text-center mb-5">
                <h1 className="fw-bold">Todos os Pontos Turísticos</h1>
            </div>

            <form className="row g-3 mb-4" onSubmit={filtrar}>
                <div className="col-md-3">
                    <input type="text" name="busca" className="form-control" placeholder="Buscar por nome" value={form.busca} onChange={alterarCampo} />
                </div>
                <div className="col-md-3">
                    <select name="categoria" className="form-select" value={form.categoria} onChange={alterarCampo}>
                        <option value="">Todas as categorias</option>
                        {categorias.map(categoria => (
                            <option key={categoria.id} value={categoria.nome}>{categoria.nome}</option>
                        ))}
                    </select>
                </div>
                <div className="col-md-2">
                    <select name="tipo" className="form-select" value={form.tipo} onChange={alterarCampo}>
                        <option value="">Todos os tipos</option>
                        <option value="cultural">Cultural</option>
                        <option value="natural">Natural</option>
                    </select>
                </div>
                <div className="col-md-3">
                    <input type="text" name="localizacao" className="form-control" placeholder="Localização" value={form.localizacao} onChange={alterarCampo} />
                </div>
                <div className="col-md-1 d-grid">
                    <button type="submit" className="btn btn-primary">Filtrar</button>
                </div>
            </form>

            <Alerta mensagem={erro} />

            {pontos.length == 0 && !erro ? (
                <div className="alert alert-secondary text-center">Nenhum ponto turístico encontrado.</div>
            ) : (
                <div className="row">
                    {pontos.map(ponto => (
                        <CardPonto ponto={ponto} logado={logado} key={ponto.id} />
                    ))}
                </div>
            )}

            <Paginacao paginacao={paginacao} onMudar={mudarPagina} />
        </>
    )
}

export default PontoPagina;
