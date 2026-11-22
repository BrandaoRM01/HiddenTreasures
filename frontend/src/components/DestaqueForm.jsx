import { useState } from "react";
import { Link } from "react-router-dom";
import { mensagemDeErro } from "../services/api";
import { mostrarMensagem } from "../services/mensagem";

export const FORM_VAZIO = {
    nome: '',
}

function DestaqueForm({ valorInicial = FORM_VAZIO, textoBotao, onSalvar }) {
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
                            Nome do Destaque <span className="text-danger">*</span>
                        </label>
                        <input type="text" id="nome" name="nome" className="form-control" placeholder="Digite o nome do destaque"
                            required value={form.nome} onChange={alterarCampo} />
                    </div>

                    <div className="d-flex gap-2">
                        <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                            {carregando ? "Salvando..." : textoBotao}
                        </button>

                        <Link to="/admin/destaques" className="btn btn-secondary w-100">
                            Voltar
                        </Link>
                    </div>
                </form>
            </div>
        </>
    )
}

export default DestaqueForm;
