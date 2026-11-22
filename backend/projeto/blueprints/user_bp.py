from flask import Blueprint, request
from projeto.controllers import UserController

user_bp = Blueprint('user', __name__)

controller = UserController()

@user_bp.route('/api/usuarios', methods=['GET', 'POST'])
def api_usuarios():
    if request.method == 'POST':
        return controller.cadastrar_usuario()
    return controller.listar_usuarios()

@user_bp.route('/api/usuarios/<email>', methods=['GET', 'PUT', 'DELETE'])
def api_usuarios_param(email):
    if request.method == 'PUT':
        return controller.editar_usuario(email)
    elif request.method == 'DELETE':
        return controller.remover_usuario(email)
    return controller.buscar_usuario_por_email(email)

@user_bp.route('/api/usuarios/auth', methods=['POST'])
def api_usuarios_auth():
    return controller.autenticar_usuario()

@user_bp.route('/api/usuarios/me', methods=['GET'])
def api_usuarios_me():
    return controller.me()

@user_bp.route('/api/usuarios/favoritos', methods=['GET', 'POST'])
def api_favoritos():
    if request.method == 'POST':
        return controller.marcar_favorito()
    return controller.listar_favoritos()

@user_bp.route('/api/usuarios/favoritos/<int:ponto_id>', methods=['DELETE'])
def api_favoritos_param(ponto_id):
    return controller.remover_favorito(ponto_id)