from flask import Blueprint, request
from projeto.controllers import CategoriaController

categorias_bp = Blueprint('categorias', __name__)

controller = CategoriaController()

@categorias_bp.route('/admin/gerenciar-categorias')
def gerenciar_categorias():
    return controller.listar_categorias()

@categorias_bp.route('/admin/cadastrar-categoria', methods=['POST', 'GET'])
def cadastrar_categoria():
    if request.method == 'POST':
        return controller.cadastrar_categoria()
    return controller.preparar_gerenciar_categorias()

@categorias_bp.route('/admin/remover-categoria/<int:id>', methods=['POST', 'GET'])
def remover_categoria(id):
    if request.method == 'POST':
        return controller.remover_categoria(id)
    return controller.preparar_gerenciar_categorias()

@categorias_bp.route('/admin/atualizar-categoria/<int:id>', methods=['POST', 'GET'])
def atualizar_categoria(id):
    if request.method == 'POST':
        return controller.atualizar_categoria(id)
    return controller.preparar_editar_categoria(id)