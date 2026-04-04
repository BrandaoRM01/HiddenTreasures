from flask import Blueprint, request
from projeto.controllers import UserController

user_bp = Blueprint('user', __name__)

controller = UserController()

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return controller.autenticar_usuario()
    return controller.preparar_login()

@user_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        return controller.cadastrar_usuario()
    return controller.preparar_cadastro()

@user_bp.route('/logout')
def logout():
    return controller.logout_usuario()

@user_bp.route('/apagar-perfil/<email>', methods=['GET'])
def apagar_perfil(email):
    return controller.apagar_perfil(email)

@user_bp.route('/favoritos')
def favoritos():
    return controller.preparar_favoritos()

@user_bp.route('/admin/painel-admin')
def painel_admin():
    return controller.preparar_painel_admin()

@user_bp.route('/admin/gerenciar-usuarios')
def gerenciar_usuarios():
    return controller.preparar_gerenciar_usuarios()

@user_bp.route('/admin/excluir-usuario/<email>', methods=['GET'])
def excluir_usuario(email):
    return controller.excluir_usuario(email)

@user_bp.route('/admin/alterar-permissao/<email>', methods=['GET'])
def alterar_permissao(email):
    return controller.alterar_permissao(email)