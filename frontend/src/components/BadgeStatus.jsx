function BadgeStatus({status, className = ""}) {
    if(status == "aprovado") {
        return <span className={`badge bg-success ${className}`}><i className="bi bi-check-circle-fill"></i> Aprovado</span>;
    }

    if(status == "rejeitado") {
        return <span className={`badge bg-danger ${className}`}><i className="bi bi-x-circle-fill"></i> Rejeitado</span>;
    }

    return <span className={`badge bg-warning text-dark ${className}`}><i className="bi bi-clock-fill"></i> Pendente</span>;
}

export default BadgeStatus;
