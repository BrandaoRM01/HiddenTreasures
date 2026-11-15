import { useEffect, useState } from "react";
import { api } from "../services/api";

// Equivalente ao usuarioModerador() do main.js.
// Devolve null enquanto não sabe, depois true (admin/superadmin) ou false (visitante/usuário comum).
function useModerador() {
    const [moderador, setModerador] = useState(localStorage.getItem("token") ? null : false);

    useEffect(() => {
        if(!localStorage.getItem("token")) {
            return;
        }

        async function verificar() {
            try {
                const res = await api.get("/api/usuarios/me");
                setModerador(res.data.tipo_usuario == "admin" || res.data.tipo_usuario == "superadmin");
            } catch (error) {
                setModerador(false);
            }
        }
        verificar();
    }, [])

    return moderador;
}

export default useModerador;
