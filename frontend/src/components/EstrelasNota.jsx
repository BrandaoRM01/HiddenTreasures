import { useState } from "react";

function EstrelasNota({ valor, onChange }) {
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
