from flask import Blueprint, request
from projeto.controllers import DestaqueController

destaques_bp = Blueprint('destaques', __name__)

controller = DestaqueController()

@destaques_bp.route('/admin/gerenciar-destaques')
def gerenciar_destaques():
    return controller.listar_destaques()

@destaques_bp.route('/admin/cadastrar-destaque', methods=['POST', 'GET'])
def cadastrar_destaque():
    if request.method == 'POST':
        return controller.cadastrar_destaque()
    return controller.preparar_gerenciar_destaques()

@destaques_bp.route('/admin/remover-destaque/<int:id>', methods=['POST', 'GET'])
def remover_destaque(id):
    if request.method == 'POST':
        return controller.remover_destaque(id)
    return controller.preparar_gerenciar_destaques()

@destaques_bp.route('/admin/atualizar-destaque/<int:id>', methods=['POST', 'GET'])
def atualizar_destaque(id):
    if request.method == 'POST':
        return controller.atualizar_destaque(id)
    return controller.preparar_editar_destaque(id)