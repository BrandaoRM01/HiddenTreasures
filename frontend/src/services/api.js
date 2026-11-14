import axios from "axios"

const URL_BACKEND = "http://localhost:5000"

export const api = axios.create({
    baseURL: URL_BACKEND,
})

// Mesma regra do apiFetch do sistema atual: se existe token, vai no header Authorization.
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("token")

    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }

    return config
})

// Imagens (pontos e fotos de usuário) continuam sendo servidas pelo Flask em /static.
export function urlEstatico(caminho) {
    return `${URL_BACKEND}/static/${caminho}`
}

export function mensagemDeErro(erro) {
    if(erro.response) {
        return erro.response.data?.mensagem ?? `Erro ${erro.response.status} na API`
    }

    if(erro.request) {
        return "Não foi possível falar com o servidor."
    }

    return erro.message
}
