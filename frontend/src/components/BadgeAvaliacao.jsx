const CORES = {
    aprovado: "bg-success",
    pendente: "bg-secondary",
    rejeitado: "bg-danger",
};

function BadgeAvaliacao({ status }) {
    return (
        <span className={`badge ${CORES[status] || "bg-secondary"}`}>
            {status.charAt(0).toUpperCase() + status.slice(1)}
        </span>
    )
}

export default BadgeAvaliacao;
