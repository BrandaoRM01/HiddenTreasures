from flask import Blueprint, request
from projeto.controllers import TipoCulturalController

tipos_culturais_bp = Blueprint('tipos_culturais', __name__)

controller = TipoCulturalController()

@tipos_culturais_bp.route('/admin/gerenciar-tipos-culturais')
def gerenciar_tipos_culturais():
    return controller.listar_tipos_culturais()

@tipos_culturais_bp.route('/admin/cadastrar-tipo-cultural', methods=['POST', 'GET'])
def cadastrar_tipo_cultural():
    if request.method == 'POST':
        return controller.cadastrar_tipo_cultural()
    return controller.preparar_gerenciar_tipos()

@tipos_culturais_bp.route('/admin/remover-tipo-cultural/<int:id>', methods=['POST', 'GET'])
def remover_tipo_cultural(id):
    if request.method == 'POST':
        return controller.remover_tipo_cultural(id)
    return controller.preparar_gerenciar_tipos()

@tipos_culturais_bp.route('/admin/atualizar-tipo-cultural/<int:id>', methods=['POST', 'GET'])
def atualizar_tipo_cultural(id):
    if request.method == 'POST':
        return controller.atualizar_tipo_cultural(id)
    return controller.preparar_editar_tipo(id)