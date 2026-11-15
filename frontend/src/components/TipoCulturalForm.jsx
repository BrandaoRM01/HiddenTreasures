import { useState } from "react";
import { NavLink } from "react-router-dom";
import { mensagemDeErro } from "../services/api";
import { mostrarMensagem } from "../services/mensagem";

export const FORM_VAZIO = {
    nome: '',
}

// Formulário compartilhado do cadastro e da edição de tipo cultural (igual ao editar_tipo_cultural.html).
//   valorInicial: valores iniciais do form (a edição só renderiza depois de carregar o registro)
//   textoBotao:   texto do botão de salvar
//   onSalvar:     async (dados) => ... ; se der erro, a mensagem do backend aparece como toast
function TipoCulturalForm({valorInicial = FORM_VAZIO, textoBotao, onSalvar}) {
    const [form, setForm] = useState(valorInicial);
    const [carregando, setCarregando] = useState(false);

    function alterarCampo(e) {
        const {name, value} = e.target;
        setForm({...form, [name]: value});
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
                            Nome do Tipo Cultural <span className="text-danger">*</span>
                        </label>
                        <input type="text" id="nome" name="nome" className="form-control" placeholder="Digite o nome do tipo cultural"
                            required value={form.nome} onChange={alterarCampo} />
                    </div>

                    <div className="d-flex gap-2">
                        <button type="submit" className="btn btn-primary w-100" disabled={carregando}>
                            {carregando ? "Salvando..." : textoBotao}
                        </button>

                        <NavLink to="/admin/tipos-culturais" className="btn btn-secondary w-100">
                            Voltar
                        </NavLink>
                    </div>
                </form>
            </div>
        </>
    )
}

export default TipoCulturalForm;
