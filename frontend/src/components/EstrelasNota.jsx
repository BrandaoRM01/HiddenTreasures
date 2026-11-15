import { useState } from "react";

// As 5 estrelas de nota (inicializarEstrelas do main.js): clique escolhe a nota e o mouse mostra uma prévia.
//   valor:    nota atual (1 a 5, ou '' quando ainda não escolheu)
//   onChange: recebe a nota escolhida
function EstrelasNota({valor, onChange}) {
    const [hover, setHover] = useState(null);

    const ativo = hover ?? (Number(valor) || 0);

    return (
        <>
            <div className="stars">
                {[1, 2, 3, 4, 5].map(estrela => (
                    <i key={estrela} className={`star ${estrela <= ativo ? "active" : ""}`} data-value={estrela}
                        onClick={() => onChange(estrela)}
                        onMouseOver={() => setHover(estrela)}
                        onMouseOut={() => setHover(null)}>★</i>
                ))}
            </div>
        </>
    )
}

export default EstrelasNota;
