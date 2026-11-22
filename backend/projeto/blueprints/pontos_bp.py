from flask import Blueprint, request
from projeto.controllers import PontoTuristicoController

pontos_bp = Blueprint('pontos', __name__)

controller = PontoTuristicoController()

@pontos_bp.route('/api/pontos', methods=['GET', 'POST'])
def api_pontos():
    if request.method == 'POST':
        return controller.cadastrar_ponto()
    return controller.listar_pontos()

@pontos_bp.route('/api/pontos/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def api_pontos_param(id):
    if request.method == 'PUT':
        return controller.editar_ponto(id)
    elif request.method == 'DELETE':
        return controller.remover_ponto(id)
    return controller.buscar_ponto(id)

@pontos_bp.route('/api/pontos/sugestoes', methods=['GET'])
def api_pontos_sugestoes():
    return controller.listar_sugestoes()

@pontos_bp.route('/api/pontos/minhas-sugestoes', methods=['GET'])
def api_minhas_sugestoes():
    return controller.listar_sugestoes_usuario()

@pontos_bp.route('/api/pontos/index', methods=['GET'])
def api_pontos_index():
    return controller.listar_index()

@pontos_bp.route('/api/pontos/detalhes/<int:id>')
def api_detalhes_ponto(id):
    return controller.detalhes_ponto_api(id)