import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, mensagemDeErro, urlEstatico } from "../services/api";
import { mostrarMensagem } from "../services/mensagem";
import Alerta from "./Alerta";

const IMAGEM_PADRAO = "img/default/hidden_treasures_logo.png";

export const FORM_VAZIO = {
    nome: '',
    localizacao: '',
    descricao: '',
    horario_funcionamento: '',
    custo_entrada: '',
    promocao: '',
    categoria: '',
    tipo_ponto: 'cultural',
    ecossistema: '',
    area_km: '',
    tipo_cultural: '',
    ano_fundacao: '',
    destaques: [],
}

export function pontoParaForm(ponto) {
    const vazio = (valor) => !valor || String(valor).trim().toLowerCase() == "não informado";

    return {
        nome: ponto.nome,
        localizacao: ponto.localizacao,
        descricao: ponto.descricao,
        horario_funcionamento: vazio(ponto.horario_funcionamento) ? '' : ponto.horario_funcionamento,
        custo_entrada: String(ponto.custo_entrada ?? ''),
        promocao: ponto.promocao ? String(ponto.promocao.id) : '',
        categoria: String(ponto.categoria.id),
        tipo_ponto: ponto.tipo_ponto,
        ecossistema: ponto.ecossistema ? String(ponto.ecossistema.id) : '',
        area_km: ponto.area_km ? String(ponto.area_km) : '',
        tipo_cultural: ponto.tipo_cultural ? String(ponto.tipo_cultural.id) : '',
        ano_fundacao: vazio(ponto.ano_fundacao) ? '' : String(ponto.ano_fundacao),
        destaques: (ponto.destaques || []).map(destaque => String(destaque.id)),
    }
}

function PontoForm({ valorInicial = FORM_VAZIO, imagemInicial = IMAGEM_PADRAO, textoFoto = "Carregar foto", textoBotao,
    rotaVoltar, limparAposSalvar = false, avisoSemCategoria, onSalvar }) {

    const [form, setForm] = useState(valorInicial);
    const [foto, setFoto] = useState(null);
    const [preview, setPreview] = useState(null);
    const [chaveFoto, setChaveFoto] = useState(0);
    const [carregando, setCarregando] = useState(false);

    const [opcoes, setOpcoes] = useState({ categorias: [], promocoes: [], ecossistemas: [], tiposCulturais: [], destaques: [] });
    const [carregandoOpcoes, setCarregandoOpcoes] = useState(true);
    const [erroOpcoes, setErroOpcoes] = useState(null);

    useEffect(() => {
        async function carregarOpcoes() {
            try {
                const [categorias, promocoes, ecossistemas, tiposCulturais, destaques] = await Promise.all([
                    api.get("/api/categorias"),
                    api.get("/api/promocoes/ativas"),
                    api.get("/api/ecossistemas"),
                    api.get("/api/tipos_culturais"),
                    api.get("/api/destaques"),
                ]);

                setOpcoes({
                    categorias: categorias.data,
                    promocoes: promocoes.data,
                    ecossistemas: ecossistemas.data,
                    tiposCulturais: tiposCulturais.data,
                    destaques: destaques.data,
                });
            } catch (error) {
                setErroOpcoes(mensagemDeErro(error));
            } finally {
                setCarregandoOpcoes(false);
            }
        }
        carregarOpcoes();
    }, [])

    useEffect(() => {
        if (!foto) {
            setPreview(null);
            return;
        }

        const url = URL.createObjectURL(foto);
        setPreview(url);

        return () => URL.revokeObjectURL(url);
    }, [foto])

    function alterarCampo(e) {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    }

    function alternarDestaque(id) {
        const idTexto = String(id);

        if (form.destaques.includes(idTexto)) {
            setForm({ ...form, destaques: form.destaques.filter(d => d != idTexto) });
            return;
        }

        if (form.destaques.length >= 3) {
            mostrarMensagem("Você pode selecionar no máximo 3 destaques.", "danger");
            return;
        }

        setForm({ ...form, destaques: [...form.destaques, idTexto] });
    }

    async function enviarForm(e) {
        e.preventDefault();

        const dados = new FormData();

        dados.append("nome", form.nome);
        dados.append("localizacao", form.localizacao);
        dados.append("descricao", form.descricao);
        dados.append("horario_funcionamento", form.horario_funcionamento);
        dados.append("custo_entrada", form.custo_entrada.replace(",", "."));
        dados.append("promocao", form.promocao);
        dados.append("categoria", form.categoria);
        dados.append("tipo_ponto", form.tipo_ponto);
        dados.append("ecossistema", form.ecossistema);
        dados.append("area_km", form.area_km);
        dados.append("tipo_cultural", form.tipo_cultural);
        dados.append("ano_fundacao", form.ano_fundacao);
        form.destaques.forEach(id => dados.append("destaques", id));

        if (foto) {
            dados.append("foto", foto);
        }

        try {
            setCarregando(true);
            await onSalvar(dados);

            if (limparAposSalvar) {
                setForm(FORM_VAZIO);
                setFoto(null);
                setChaveFoto(chaveFoto + 1);
            }
        }
        catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
        finally {
            setCarregando(false);
        }
    }

    if (carregandoOpcoes) {
        return (<p className="text-muted">Carregando...</p>);
    }

    if (erroOpcoes) {
        return (<Alerta mensagem={erroOpcoes} />);
    }

    if (opcoes.categorias.length == 0) {
        return avisoSemCategoria ?? (
            <div className="card p-4 mb-4 shadow">
                <div className="alert alert-info text-center mb-0">Nenhuma categoria cadastrada.</div>
            </div>
        );
    }

    const ehNatural = form.tipo_ponto == "natural";

    return (
        <>
            <div className="card p-4 mb-4 shadow">
                <form onSubmit={enviarForm}>

                    <div className="text-center mb-4">
                        <label htmlFor="foto-imagem" style={{ cursor: "pointer" }}>
                            <img src={preview ?? urlEstatico(imagemInicial)} alt="Imagem do ponto" className="rounded shadow"
                                style={{ width: "150px", height: "150px", objectFit: "cover" }} />
                        </label>

                        <input key={chaveFoto} name="foto" type="file" hidden id="foto-imagem" accept="image/*"
                            onChange={(e) => setFoto(e.target.files[0] ?? null)} />

                        <div className="mt-2">
                            <label className="btn btn-outline-primary btn-sm mt-2" htmlFor="foto-imagem">
                                <i className="bi bi-upload"></i> {textoFoto}
                            </label>
                        </div>
                    </div>

                    <div className="mb-3">
                        <label htmlFor="nome" className="form-label">Nome do Ponto <span className="text-danger">*</span></label>
                        <input id="nome" name="nome" type="text" className="form-control" placeholder="Digite o nome" required
                            value={form.nome} onChange={alterarCampo} />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="localizacao" className="form-label">Localização <span className="text-danger">*</span></label>
                        <input id="localizacao" name="localizacao" type="text" className="form-control" placeholder="Digite a localização" required
                            value={form.localizacao} onChange={alterarCampo} />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="descricao" className="form-label">Descrição <span className="text-danger">*</span></label>
                        <textarea id="descricao" name="descricao" className="form-control" rows="3" placeholder="Descreva o ponto turístico" required
                            value={form.descricao} onChange={alterarCampo}></textarea>
                    </div>

                    <div className="row">
                        <div className="col-md-6">
                            <div className="mb-3">
                                <label htmlFor="horario_funcionamento" className="form-label">Horário de Funcionamento</label>
                                <input id="horario_funcionamento" name="horario_funcionamento" type="text" className="form-control" placeholder="Ex: 08:00 às 18:00"
                                    value={form.horario_funcionamento} onChange={alterarCampo} />
                            </div>
                        </div>

                        <div className="col-md-6">
                            <div className="mb-3">
                                <label htmlFor="custo_entrada" className="form-label">Custo de Entrada (R$)</label>
                                <input id="custo_entrada" name="custo_entrada" type="text" className="form-control" placeholder="Ex: 20,00"
                                    value={form.custo_entrada} onChange={alterarCampo} />
                            </div>
                        </div>
                    </div>

                    {opcoes.promocoes.length > 0 && (
                        <div className="mb-3">
                            <label htmlFor="promocao" className="form-label">Promoção</label>
                            <select id="promocao" name="promocao" className="form-control" value={form.promocao} onChange={alterarCampo}>
                                <option value="">Nenhuma</option>
                                {opcoes.promocoes.map(promocao => (
                                    <option key={promocao.id} value={promocao.id}>{promocao.titulo}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    <div className="mb-3">
                        <label htmlFor="categoria" className="form-label">Categoria <span className="text-danger">*</span></label>
                        <select id="categoria" name="categoria" className="form-control" required value={form.categoria} onChange={alterarCampo}>
                            <option value="">Selecione a categoria</option>
                            {opcoes.categorias.map(categoria => (
                                <option key={categoria.id} value={categoria.id}>{categoria.nome}</option>
                            ))}
                        </select>
                    </div>

                    {opcoes.destaques.length > 0 && (
                        <div className="mb-3">
                            <label className="form-label">Destaques <span className="text-muted">(máximo 3)</span></label>

                            <div className="d-flex flex-wrap gap-2">
                                {opcoes.destaques.map(destaque => (
                                    <span key={destaque.id}>
                                        <input type="checkbox" className="btn-check destaque-checkbox" id={`destaque${destaque.id}`} name="destaques"
                                            value={destaque.id} autoComplete="off"
                                            checked={form.destaques.includes(String(destaque.id))}
                                            onChange={() => alternarDestaque(destaque.id)} />
                                        <label className="btn btn-outline-primary destaque-chip" htmlFor={`destaque${destaque.id}`}>{destaque.nome}</label>
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="mb-3">
                        <label htmlFor="tipo_ponto" className="form-label">Tipo do Ponto <span className="text-danger">*</span></label>
                        <select id="tipo_ponto" name="tipo_ponto" className="form-control" required value={form.tipo_ponto} onChange={alterarCampo}>
                            <option value="cultural">Ponto Cultural</option>
                            <option value="natural">Ponto Natural</option>
                        </select>
                    </div>

                    <div id="campos-natural" className={ehNatural ? "" : "d-none"}>
                        <div className="mb-3">
                            <label htmlFor="ecossistema" className="form-label">Ecossistema</label>
                            <select id="ecossistema" name="ecossistema" className="form-control" value={form.ecossistema} onChange={alterarCampo}>
                                <option value="">Selecione um ecossistema</option>
                                {opcoes.ecossistemas.map(ecossistema => (
                                    <option key={ecossistema.id} value={ecossistema.id}>{ecossistema.nome}</option>
                                ))}
                            </select>
                        </div>

                        <div className="mb-3">
                            <label htmlFor="area_km" className="form-label">Área (km²)</label>
                            <input id="area_km" name="area_km" type="number" step="0.01" className="form-control" placeholder="Ex: 125.50"
                                value={form.area_km} onChange={alterarCampo} />
                        </div>
                    </div>

                    <div id="campos-cultural" className={ehNatural ? "d-none" : ""}>
                        <div className="mb-3">
                            <label htmlFor="tipo_cultural" className="form-label">Tipo Cultural</label>
                            <select id="tipo_cultural" name="tipo_cultural" className="form-control" value={form.tipo_cultural} onChange={alterarCampo}>
                                <option value="">Selecione um tipo</option>
                                {opcoes.tiposCulturais.map(tipo => (
                                    <option key={tipo.id} value={tipo.id}>{tipo.nome}</option>
                                ))}
                            </select>
                        </div>

                        <div className="mb-3">
                            <label htmlFor="ano_fundacao" className="form-label">Ano de Fundação</label>
                            <input id="ano_fundacao" name="ano_fundacao" className="form-control" placeholder="Ex: 1895"
                                value={form.ano_fundacao} onChange={alterarCampo} />
                        </div>
                    </div>

                    {rotaVoltar ? (
                        <div className="d-flex gap-2">
                            <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                                {carregando ? "Salvando..." : textoBotao}
                            </button>

                            <Link to={rotaVoltar} className="btn btn-secondary w-100">Voltar</Link>
                        </div>
                    ) : (
                        <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                            {carregando ? "Salvando..." : textoBotao}
                        </button>
                    )}

                </form>
            </div>
        </>
    )
}

export default PontoForm;
