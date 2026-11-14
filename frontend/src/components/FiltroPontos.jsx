import { useEffect, useState } from "react";
import { api } from "../services/api";

const FILTRO_VAZIO = { busca: "", categoria: "", tipo: "", localizacao: "", status: "" };

function FiltroPontos({ onFiltrar }) {
    const [form, setForm] = useState(FILTRO_VAZIO);
    const [categorias, setCategorias] = useState([]);

    useEffect(() => {
        async function carregarCategorias() {
            try {
                const res = await api.get("/api/categorias");
                setCategorias(res.data);
            } catch (error) {
                // sem as categorias o filtro continua funcionando, só fica sem as opções do select
            }
        }
        carregarCategorias();
    }, [])

    function alterarCampo(e) {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    }

    function filtrar(e) {
        e.preventDefault();

        onFiltrar({
            ...form,
            busca: form.busca.trim(),
            localizacao: form.localizacao.trim(),
        });
    }

    return (
        <>
            <div className="p-3 mb-4">
                <form className="row g-3" onSubmit={filtrar}>
                    <div className="col-md-3">
                        <input type="text" name="busca" className="form-control" placeholder="Buscar por nome"
                            value={form.busca} onChange={alterarCampo} />
                    </div>

                    <div className="col-md-2">
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

                    <div className="col-md-2">
                        <input type="text" name="localizacao" className="form-control" placeholder="Localização"
                            value={form.localizacao} onChange={alterarCampo} />
                    </div>

                    <div className="col-md-2">
                        <select name="status" className="form-select" value={form.status} onChange={alterarCampo}>
                            <option value="">Todos os status</option>
                            <option value="aprovado">Aprovado</option>
                            <option value="pendente">Pendente</option>
                            <option value="rejeitado">Rejeitado</option>
                        </select>
                    </div>

                    <div className="col-md-1 d-grid">
                        <button type="submit" className="btn btn-primary">Filtrar</button>
                    </div>
                </form>
            </div>
        </>
    )
}

export default FiltroPontos;
