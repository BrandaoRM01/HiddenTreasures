from flask import Blueprint, request
from projeto.controllers import AvaliacaoController

avaliacoes_bp = Blueprint('avaliacoes', __name__)

controller = AvaliacaoController()

@avaliacoes_bp.route('/api/avaliacoes/ponto/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_avaliacoes_ponto(id):
    if request.method == 'POST':
        return controller.cadastrar_avaliacao(id)
    elif request.method == 'PUT':
        return controller.atualizar_avaliacao(id)
    elif request.method == 'DELETE':
        return controller.remover_avaliacao(id)
    return controller.listar_avaliacoes_ponto(id)