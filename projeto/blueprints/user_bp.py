from flask import Blueprint, jsonify, request, session
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

@user_bp.route('/logout')
def logout():
    return controller.logout_usuario()

@user_bp.route('/apagar-perfil/<email>', methods=['GET'])
def apagar_perfil(email):
    return controller.apagar_perfil(email)

@user_bp.route('/admin/painel-admin')
def painel_admin():
    return controller.preparar_painel_admin()

@user_bp.route('/admin/gerenciar-usuarios')
def gerenciar_usuarios():
    return controller.preparar_gerenciar_usuarios()

@user_bp.route('/admin/excluir-usuario/<email>', methods=['GET'])
def excluir_usuario(email):
    return controller.excluir_usuario(email)

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
    if email == 'me':
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        email = session['usuario']['email']

    if request.method == 'PUT':
        return controller.editar_usuario(email)
    elif request.method == 'DELETE':
        return controller.remover_usuario(email)
    return controller.buscar_usuario_por_email(email)

@user_bp.route('/api/usuarios/auth', methods=['GET', 'POST'])
def api_usuarios_auth():
    if request.method == 'POST':
        return controller.autenticar_usuario()

@user_bp.route('/api/usuarios/favoritos', methods=['GET', 'POST'])
def api_favoritos():
    if request.method == 'POST':
        return controller.alterar_favorito()
    return controller.listar_favoritos()