from flask import Flask
from projeto.config import Config
from projeto.dao import UserDAO, PromocaoDAO

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

        user_dao.criar_usuario_superadmin()
        promocao_dao.deletar_promocoes_expiradas()

    return app