import { useState } from "react";

// Input de senha com botão de mostrar/ocultar (substitui o toggle-password + olho do main.js)
function CampoSenha({id, name, rotulo, valor, onChange, autoComplete}) {
    const [visivel, setVisivel] = useState(false);

    return (
        <>
            <div className="mb-3">
                <label className="form-label" htmlFor={id}>
                    {rotulo} <span className="text-danger">*</span>
                </label>

                <div className="input-group">
                    <input id={id} name={name} type={visivel ? "text" : "password"} className="form-control"
                        value={valor} onChange={onChange} autoComplete={autoComplete} />

                    <button type="button" className="btn btn-outline-secondary" onClick={() => setVisivel(!visivel)}
                        aria-label={visivel ? "Ocultar senha" : "Mostrar senha"}>
                        <i className={`bi ${visivel ? "bi-eye-slash" : "bi-eye"}`}></i>
                    </button>
                </div>
            </div>
        </>
    )
}

export default CampoSenha;
