import { protegerRota } from '../main.js';

document.addEventListener('DOMContentLoaded', async () => {
    let usuario = await protegerRota(['admin', 'superadmin']);
    if (!usuario) return;

    configurarLinksDoPainel();
});

function configurarLinksDoPainel() {
    const links = {
        'link-gerenciar-categorias': '/admin/gerenciar-categorias',
        'link-gerenciar-pontos': '/admin/gerenciar-pontos',
        'link-gerenciar-promocoes': '/admin/gerenciar-promocoes',
        'link-gerenciar-usuarios': '/admin/gerenciar-usuarios',
        'link-gerenciar-ecossistemas': '/admin/gerenciar-ecossistemas',
        'link-gerenciar-tipos-culturais': '/admin/gerenciar-tipos-culturais',
        'link-gerenciar-destaques': '/admin/gerenciar-destaques',
        'link-gerenciar-sugestoes': '/admin/gerenciar-sugestoes'
    };

    for (let id in links) {
        document.getElementById(id).addEventListener('click', (evento) => {
            evento.preventDefault();
            window.location.href = links[id];
        });
    }
}