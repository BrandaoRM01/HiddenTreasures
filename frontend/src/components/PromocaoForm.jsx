import { useState } from "react";
import { Link } from "react-router-dom";
import { mensagemDeErro } from "../services/api";
import { mostrarMensagem } from "../services/mensagem";

export const FORM_VAZIO = {
    titulo: '',
    descricao: '',
    desconto: '',
    data_inicio: '',
    data_fim: '',
}

function PromocaoForm({ valorInicial = FORM_VAZIO, textoBotao, onSalvar }) {
    const [form, setForm] = useState(valorInicial);
    const [carregando, setCarregando] = useState(false);

    function alterarCampo(e) {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    }

    async function enviarForm(e) {
        e.preventDefault();

        const dados = {
            titulo: form.titulo,
            descricao: form.descricao,
            desconto: form.desconto,
            data_inicio: form.data_inicio,
            data_fim: form.data_fim,
        }

        try {
            setCarregando(true);
            await onSalvar(dados);
        }
        catch (error) {
            mostrarMensagem(mensagemDeErro(error), "danger");
        }
        finally {
            setCarregando(false);
        }
    }

    return (
        <>
            <div className="card p-4 shadow">
                <form onSubmit={enviarForm}>
                    <div className="mb-3">
                        <label htmlFor="titulo" className="form-label">
                            Título da Promoção <span className="text-danger">*</span>
                        </label>
                        <input id="titulo" name="titulo" type="text" className="form-control" placeholder="Digite o título da promoção"
                            required value={form.titulo} onChange={alterarCampo} />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="descricao" className="form-label">
                            Descrição
                        </label>
                        <textarea id="descricao" name="descricao" className="form-control" rows="3" placeholder="Descreva a promoção"
                            value={form.descricao} onChange={alterarCampo}></textarea>
                    </div>

                    <div className="mb-3">
                        <label htmlFor="desconto" className="form-label">
                            Desconto (%) <span className="text-danger">*</span>
                        </label>
                        <input id="desconto" name="desconto" type="number" step="0.01" className="form-control" placeholder="Ex: 10"
                            required value={form.desconto} onChange={alterarCampo} />
                    </div>

                    <div className="row">
                        <div className="col-md-6">
                            <div className="mb-3">
                                <label htmlFor="data_inicio" className="form-label">
                                    Data de Início <span className="text-danger">*</span>
                                </label>
                                <input id="data_inicio" name="data_inicio" type="date" className="form-control"
                                    required value={form.data_inicio} onChange={alterarCampo} />
                            </div>
                        </div>

                        <div className="col-md-6">
                            <div className="mb-3">
                                <label htmlFor="data_fim" className="form-label">
                                    Data de Fim <span className="text-danger">*</span>
                                </label>
                                <input id="data_fim" name="data_fim" type="date" className="form-control"
                                    required value={form.data_fim} onChange={alterarCampo} />
                            </div>
                        </div>
                    </div>

                    <div className="d-flex gap-2 mt-3">
                        <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                            {carregando ? "Salvando..." : textoBotao}
                        </button>

                        <Link to="/admin/promocoes" className="btn btn-secondary w-100">
                            Voltar
                        </Link>
                    </div>
                </form>
            </div>
        </>
    )
}

export default PromocaoForm;
