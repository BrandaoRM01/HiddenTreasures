from flask import Blueprint, request
from projeto.controllers import EcossistemaController

ecossistemas_bp = Blueprint('ecossistemas', __name__)

controller = EcossistemaController()

@ecossistemas_bp.route('/api/ecossistemas', methods=['GET', 'POST'])
def api_ecossistemas():
    if request.method == 'POST':
        return controller.cadastrar_ecossistema()
    return controller.listar_ecossistemas()

@ecossistemas_bp.route('/api/ecossistemas/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def api_ecossistemas_param(id):
    if request.method == 'DELETE':
        return controller.remover_ecossistema(id)
    elif request.method == 'PUT':
        return controller.atualizar_ecossistema(id)
    return controller.buscar_ecossistema_por_id(id)