import { useEffect, useRef, useState } from "react";

function Dropdown({ classeBotao, rotuloBotao, itens }) {
    const [aberto, setAberto] = useState(false);
    const ref = useRef(null);

    useEffect(() => {
        if (!aberto) {
            return;
        }

        function aoClicarFora(e) {
            if (ref.current && !ref.current.contains(e.target)) {
                setAberto(false);
            }
        }

        document.addEventListener("mousedown", aoClicarFora);

        return () => document.removeEventListener("mousedown", aoClicarFora);
    }, [aberto])

    return (
        <>
            <div className="dropdown" ref={ref}>
                <button type="button" className={classeBotao} aria-expanded={aberto} onClick={() => setAberto(!aberto)}>
                    {rotuloBotao}
                </button>

                <ul className={`dropdown-menu dropdown-menu-end ${aberto ? "show" : ""}`} data-bs-popper="static">
                    {itens.map(item => (
                        <li key={item.texto}>
                            <a href="#" className={`dropdown-item ${item.classe ?? ""}`}
                                onClick={(e) => { e.preventDefault(); setAberto(false); item.onClick(); }}>
                                {item.texto}
                            </a>
                        </li>
                    ))}
                </ul>
            </div>
        </>
    )
}

export default Dropdown;
