from flask import Blueprint, request
from projeto.controllers import EcossistemaController

ecossistemas_bp = Blueprint('ecossistemas', __name__)

controller = EcossistemaController()

@ecossistemas_bp.route('/admin/gerenciar-ecossistemas')
def gerenciar_ecossistemas():
    return controller.listar_ecossistemas()

@ecossistemas_bp.route('/admin/cadastrar-ecossistema', methods=['POST', 'GET'])
def cadastrar_ecossistema():
    if request.method == 'POST':
        return controller.cadastrar_ecossistema()
    return controller.preparar_gerenciar_ecossistemas()

@ecossistemas_bp.route('/admin/remover-ecossistema/<int:id>', methods=['POST', 'GET'])
def remover_ecossistema(id):
    if request.method == 'POST':
        return controller.remover_ecossistema(id)
    return controller.preparar_gerenciar_ecossistemas()

@ecossistemas_bp.route('/admin/atualizar-ecossistema/<int:id>', methods=['POST', 'GET'])
def atualizar_ecossistema(id):
    if request.method == 'POST':
        return controller.atualizar_ecossistema(id)
    return controller.preparar_editar_ecossistema(id)