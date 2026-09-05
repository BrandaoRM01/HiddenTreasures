from flask import Blueprint, request
from projeto.controllers import HistoricoSenhaController

historico_senhas_bp = Blueprint('historico_senhas', __name__)

controller = HistoricoSenhaController()

@historico_senhas_bp.route('/recuperar-senha')
def recuperar_senha():
    return controller.preparar_recuperar_senha()

@historico_senhas_bp.route('/redefinir-senha/<token>')
def redefinir_senha(token):
    return controller.preparar_redefinir_senha(token)

@historico_senhas_bp.route('/api/recuperacao-senha', methods=['POST'])
def api_enviar_recuperacao():
    return controller.enviar_recuperacao()

@historico_senhas_bp.route('/api/redefinir-senha/<token>', methods=['POST'])
def api_redefinir_senha(token):
    return controller.redefinir_senha(token)