from flask import Blueprint, request
from projeto.controllers import HistoricoSenhaController

historico_senhas_bp = Blueprint('historico_senhas', __name__)

controller = HistoricoSenhaController()

@historico_senhas_bp.route('/recuperar-senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        return controller.enviar_recuperacao()
    return controller.preparar_recuperar_senha()

@historico_senhas_bp.route('/redefinir-senha/<token>', methods=['GET', 'POST'])
def redefinir_senha(token):
    if request.method == 'POST':
        return controller.redefinir_senha(token)
    return controller.preparar_redefinir_senha(token)