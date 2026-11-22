import { useState } from "react";
import { Link } from "react-router-dom";
import { mensagemDeErro } from "../services/api";
import { mostrarMensagem } from "../services/mensagem";

export const FORM_VAZIO = {
    nome: '',
    descricao: '',
}

function CategoriaForm({ valorInicial = FORM_VAZIO, textoBotao, onSalvar }) {
    const [form, setForm] = useState(valorInicial);
    const [carregando, setCarregando] = useState(false);

    function alterarCampo(e) {
        const { name, value } = e.target;
        setForm({ ...form, [name]: value });
    }

    async function enviarForm(e) {
        e.preventDefault();

        const dados = {
            nome: form.nome,
            descricao: form.descricao,
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
            <div className="card shadow p-4">
                <form onSubmit={enviarForm}>
                    <div className="mb-3">
                        <label htmlFor="nome" className="form-label">
                            Nome da Categoria <span className="text-danger">*</span>
                        </label>
                        <input type="text" id="nome" name="nome" className="form-control" placeholder="Digite o nome da categoria"
                            required value={form.nome} onChange={alterarCampo} />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="descricao" className="form-label">
                            Descrição
                        </label>
                        <textarea id="descricao" name="descricao" className="form-control" rows="3" placeholder="Digite uma descrição"
                            value={form.descricao} onChange={alterarCampo}></textarea>
                    </div>

                    <div className="d-flex gap-2">
                        <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                            {carregando ? "Salvando..." : textoBotao}
                        </button>

                        <Link to="/admin/categorias" className="btn btn-secondary w-100">
                            Voltar
                        </Link>
                    </div>
                </form>
            </div>
        </>
    )
}

export default CategoriaForm;
