from projeto.models import HistoricoSenha

class HistoricoSenhaFactory:

    @staticmethod
    def criar_historico_senha(usuario, senha_hash, criado_em=None):
        return HistoricoSenha(usuario=usuario, senha_hash=senha_hash, criado_em=criado_em)