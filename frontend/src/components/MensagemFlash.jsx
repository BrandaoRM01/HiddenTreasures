import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ICONES = {
    success: "bi-check-circle-fill",
    danger: "bi-x-circle-fill",
    warning: "bi-exclamation-triangle-fill",
    info: "bi-info-circle-fill",
};

// Toasts do sistema (mesmas classes .alerta-toast / #container-alertas do index.css).
// Duas formas de disparar um toast:
//   1) mostrarMensagem(mensagem, classe)                    -> de qualquer lugar (services/mensagem.js)
//   2) navigate("/rota", {state: {mensagem, classe}})       -> aparece na página de destino
//      (a RotaProtegida já usa esse formato)
function MensagemFlash() {
    const location = useLocation();
    const navigate = useNavigate();
    const [avisos, setAvisos] = useState([]);

    function remover(id) {
        setAvisos(atuais => atuais.filter(aviso => aviso.id != id));
    }

    function adicionar(mensagem, classe = "info") {
        const id = Date.now() + Math.random();

        setAvisos(atuais => [...atuais, {id, mensagem, classe}]);
        setTimeout(() => remover(id), 4000);
    }

    // mensagem vinda de navigate(..., {state})
    useEffect(() => {
        if(location.state?.mensagem) {
            adicionar(location.state.mensagem, location.state.classe);

            // limpa o state da navegação para a mensagem não reaparecer ao dar F5
            navigate(location.pathname + location.search, {replace: true, state: null});
        }
    }, [location.key])

    // mensagem vinda de mostrarMensagem()
    useEffect(() => {
        function aoReceber(e) {
            adicionar(e.detail.mensagem, e.detail.classe);
        }

        window.addEventListener("mensagem-flash", aoReceber);

        return () => window.removeEventListener("mensagem-flash", aoReceber);
    }, [])

    return (
        <>
            <div id="container-alertas">
                {avisos.map(aviso => (
                    <div className={`alerta-toast alerta-${aviso.classe}`} role="alert" key={aviso.id}>
                        <i className={`bi ${ICONES[aviso.classe] ?? ICONES.info} icone`}></i>
                        <span className="mensagem">{aviso.mensagem}</span>
                        <button type="button" className="fechar" onClick={() => remover(aviso.id)}>&times;</button>
                    </div>
                ))}
            </div>
        </>
    )
}

export default MensagemFlash;
