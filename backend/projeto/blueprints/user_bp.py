from flask import Blueprint, request
from projeto.controllers import UserController

user_bp = Blueprint('user', __name__)

controller = UserController()

@user_bp.route('/login')
def login():
    return controller.preparar_login()

@user_bp.route('/cadastro')
def cadastro():
    return controller.preparar_cadastro()

@user_bp.route('/editar-perfil')
def editar_perfil():
    return controller.preparar_editar_perfil()

@user_bp.route('/logout', methods=['POST'])
def logout():
    return controller.logout_usuario()

@user_bp.route('/admin/painel-admin')
def painel_admin():
    return controller.preparar_painel_admin()

@user_bp.route('/admin/gerenciar-usuarios')
def gerenciar_usuarios():
    return controller.preparar_gerenciar_usuarios()

@user_bp.route('/favoritos')
def favoritos():
    return controller.preparar_favoritos()

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