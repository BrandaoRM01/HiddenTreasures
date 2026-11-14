from projeto.models import Destaque

class DestaqueFactory:

    @staticmethod
    def criar_destaque(nome, id=None):
        return Destaque(nome=nome, id=id)