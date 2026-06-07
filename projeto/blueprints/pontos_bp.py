from flask import Blueprint, request
from projeto.controllers import PontoTuristicoController

pontos_bp = Blueprint('pontos', __name__)

controller = PontoTuristicoController()

@pontos_bp.route('/')
def index():
    return controller.preparar_index()

@pontos_bp.route('/sobre')
def sobre():
    return controller.preparar_sobre()

@pontos_bp.route('/pontos')
def pontos():
    return controller.preparar_pontos_turisticos()

@pontos_bp.route('/admin/gerenciar-pontos')
def gerenciar_pontos():
    return controller.preparar_gerenciar_pontos()

@pontos_bp.route('/admin/gerenciar-sugestoes')
def gerenciar_sugestoes():
    return controller.preparar_gerenciar_sugestoes()

@pontos_bp.route('/admin/cadastrar-pontos', methods=['GET', 'POST'])
def cadastrar_ponto():
    if request.method == 'POST':
        return controller.cadastrar_ponto()
    return controller.preparar_gerenciar_pontos()

@pontos_bp.route('/admin/remover-ponto/<int:id>', methods=['GET', 'POST'])
def remover_ponto(id):
    if request.method == 'POST':
        return controller.remover_ponto(id)
    return controller.preparar_gerenciar_pontos()

@pontos_bp.route('/admin/editar-ponto/<int:id>', methods=['GET', 'POST'])
def editar_ponto(id):
    if request.method == 'POST':
        return controller.editar_ponto(id)
    return controller.preparar_editar_ponto(id)

@pontos_bp.route('/detalhes-ponto/<int:id>')
def detalhes_ponto(id):
    return controller.preparar_detalhes_ponto(id)

@pontos_bp.route('/buscar-pontos', methods=['GET', 'POST'])
def buscar_pontos():
    if request.method == 'POST':
        return controller.listar_pontos_busca()
    return controller.preparar_index()

@pontos_bp.route('/sugerir-ponto', methods=['GET', 'POST'])
def sugerir_ponto():
    if request.method == 'POST':
        return controller.sugerir_ponto()
    return controller.preparar_sugerir_ponto()

@pontos_bp.route('/editar-sugestao/<int:id>', methods=['GET', 'POST'])
def editar_sugestao(id):
    if request.method == 'POST':
        return controller.editar_ponto(id)
    return controller.preparar_editar_sugestao(id)

@pontos_bp.route('/admin/alterar-status-sugestao/<int:id_ponto>/<string:status>', methods=['POST','GET'])
def alterar_status_sugestao(id_ponto, status):
    if request.method == 'POST':
        return controller.alterar_status(id_ponto, status)
    return controller.preparar_gerenciar_pontos()