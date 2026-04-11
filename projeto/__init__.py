from flask import Flask
from projeto.config import Config
from projeto.models import HistoricoSenha
from projeto.dao import UserDAO, PromocaoDAO, HistoricoSenhaDAO
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from projeto.blueprints import user_bp, pontos_bp, categorias_bp, avaliacoes_bp, promocoes_bp, favoritos_bp

    app.register_blueprint(pontos_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(avaliacoes_bp)
    app.register_blueprint(promocoes_bp)
    app.register_blueprint(favoritos_bp)

    with app.app_context():
        user_dao = UserDAO()
        promocao_dao = PromocaoDAO()
        historico_senha_dao = HistoricoSenhaDAO()

        user_dao.criar_usuario_superadmin()

        usuario = user_dao.buscar_usuario_por_email(Config.SUPERADMIN_EMAIL)
        senha = Config.SUPERADMIN_PASSWORD

        if not historico_senha_dao.senha_existe(usuario, senha):
            senha_hash = generate_password_hash(Config.SUPERADMIN_PASSWORD)

            historico = HistoricoSenha(usuario, senha_hash)
    
            historico_senha_dao.inserir_nova_senha(historico)

        promocao_dao.deletar_promocoes_expiradas()

    return app