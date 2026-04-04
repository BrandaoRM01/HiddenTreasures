from flask import Blueprint, request
from projeto.controllers import PromocaoController

promocoes_bp = Blueprint('promocoes', __name__)

controller = PromocaoController()

@promocoes_bp.route('/admin/gerenciar-promocoes')
def gerenciar_promocoes():
    return controller.preparar_gerenciar_promocoes()

@promocoes_bp.route('/admin/cadastrar-promocao', methods=['GET', 'POST'])
def cadastrar_promocao():
    if request.method == 'POST':
        return controller.cadastrar_promocao()
    return controller.preparar_gerenciar_promocoes()

@promocoes_bp.route('/admin/remover-promocao/<int:id>', methods=['GET', 'POST'])
def remover_promocao(id):
    if request.method == 'POST':
        return controller.remover_promocao(id)
    return controller.preparar_gerenciar_promocoes()

@promocoes_bp.route('/admin/editar-promocao/<int:id>', methods=['GET', 'POST'])
def editar_promocao(id):
    if request.method == 'POST':
        return controller.editar_promocao(id)
    return controller.preparar_editar_promocao(id)