from flask import Blueprint, request
from projeto.controllers import PromocaoController

promocoes_bp = Blueprint('promocoes', __name__)

controller = PromocaoController()

@promocoes_bp.route('/admin/gerenciar-promocoes')
def gerenciar_promocoes():
    return controller.preparar_gerenciar_promocoes()

@promocoes_bp.route('/admin/editar-promocao/<int:id>')
def editar_promocao(id):
    return controller.preparar_editar_promocao(id)

@promocoes_bp.route('/api/promocoes', methods=['GET', 'POST'])
def api_ecossistemas():
    if request.method == 'POST':
        return controller.cadastrar_promocao()
    return controller.listar_promocoes()

@promocoes_bp.route('/api/promocoes/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def api_ecossistemas_param(id):
    if request.method == 'DELETE':
        return controller.remover_promocao(id)
    elif request.method == 'PUT':
        return controller.editar_promocao(id)
    return controller.buscar_promocao_por_id(id)