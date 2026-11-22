from flask import Blueprint, request
from projeto.controllers import PromocaoController

promocoes_bp = Blueprint('promocoes', __name__)

controller = PromocaoController()

@promocoes_bp.route('/api/promocoes', methods=['GET', 'POST'])
def api_promocoes():
    if request.method == 'POST':
        return controller.cadastrar_promocao()
    return controller.listar_promocoes()

@promocoes_bp.route('/api/promocoes/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def api_promocoes_param(id):
    if request.method == 'DELETE':
        return controller.remover_promocao(id)
    elif request.method == 'PUT':
        return controller.editar_promocao(id)
    return controller.buscar_promocao_por_id(id)

@promocoes_bp.route('/api/promocoes/ativas', methods=['GET'])
def api_promocoes_ativas():
    return controller.listar_promocoes_ativas()