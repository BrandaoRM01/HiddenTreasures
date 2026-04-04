from flask import Blueprint, request
from projeto.controllers import AvaliacaoController

avaliacoes_bp = Blueprint('avaliacoes', __name__)

controller = AvaliacaoController()

@avaliacoes_bp.route('/avaliar-ponto/<int:id>', methods=['GET', 'POST'])
def avaliar_ponto(id):
    if request.method == 'POST':
        return controller.cadastrar_avaliacao(id)
    return controller.preparar_detalhes_ponto(id)

@avaliacoes_bp.route('/editar-avaliacao/<int:id>', methods=['GET', 'POST'])
def editar_avaliacao(id):
    if request.method == 'POST':
        return controller.atualizar_avaliacao(id)
    return controller.preparar_editar_avaliacao(id)

@avaliacoes_bp.route('/excluir-avaliacao/<usuario_email>/<int:id>', methods=['POST'])
def excluir_avaliacao(usuario_email, id):
    if request.method == 'POST':
        return controller.remover_avaliacao(usuario_email, id)
    return controller.preparar_detalhes_ponto(id)

@avaliacoes_bp.route('/avaliacoes-ponto/<int:id>')
def avaliacoes_ponto(id):
    return controller.preparar_avaliacoes_ponto(id)