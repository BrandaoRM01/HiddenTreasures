from flask import Blueprint, request
from projeto.controllers import TipoCulturalController

tipos_culturais_bp = Blueprint('tipos_culturais', __name__)

controller = TipoCulturalController()

@tipos_culturais_bp.route('/admin/gerenciar-tipos-culturais')
def gerenciar_tipos_culturais():
    return controller.preparar_gerenciar_tipos()

@tipos_culturais_bp.route('/admin/atualizar-tipo-cultural/<int:id>')
def atualizar_tipo_cultural(id):
    return controller.preparar_editar_tipo(id)

@tipos_culturais_bp.route('/api/tipos_culturais', methods=['GET', 'POST'])
def api_tipos_culturais():
    if request.method == 'POST':
        return controller.cadastrar_tipo_cultural()
    return controller.listar_tipos_culturais()

@tipos_culturais_bp.route('/api/tipos_culturais/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def api_tipos_culturais_param(id):
    if request.method == 'DELETE':
        return controller.remover_tipo_cultural(id)
    elif request.method == 'PUT':
        return controller.atualizar_tipo_cultural(id)
    return controller.buscar_tipo_cultural_por_id(id)