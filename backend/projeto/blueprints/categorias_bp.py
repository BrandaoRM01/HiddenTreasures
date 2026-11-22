from flask import Blueprint, request
from projeto.controllers import CategoriaController

categorias_bp = Blueprint('categorias', __name__)

controller = CategoriaController()

@categorias_bp.route('/api/categorias', methods=['GET', 'POST'])
def api_categorias():
    if request.method == 'POST':
        return controller.cadastrar_categoria()
    return controller.listar_categorias()

@categorias_bp.route('/api/categorias/<int:id>', methods=['DELETE', 'PUT', 'GET'])
def api_categoria_param(id):
    if request.method == 'DELETE':
        return controller.remover_categoria(id)
    elif request.method == 'PUT':
        return controller.atualizar_categoria(id)
    return controller.buscar_categoria_por_id(id)