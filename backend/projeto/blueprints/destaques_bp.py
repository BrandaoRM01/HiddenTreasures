from flask import Blueprint, request
from projeto.controllers import DestaqueController

destaques_bp = Blueprint('destaques', __name__)

controller = DestaqueController()

@destaques_bp.route('/admin/gerenciar-destaques')
def gerenciar_destaques():
    return controller.preparar_gerenciar_destaques()

@destaques_bp.route('/admin/atualizar-destaque/<int:id>')
def atualizar_destaque(id):
    return controller.preparar_editar_destaque(id)

@destaques_bp.route('/api/destaques', methods=['GET', 'POST'])
def api_destaques():
    if request.method == 'POST':
        return controller.cadastrar_destaque()
    return controller.listar_destaques()

@destaques_bp.route('/api/destaques/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def api_destaques_param(id):
    if request.method == 'PUT':
        return controller.atualizar_destaque(id)
    elif request.method == 'DELETE':
        return controller.remover_destaque(id)
    return controller.buscar_destaque_por_id(id)