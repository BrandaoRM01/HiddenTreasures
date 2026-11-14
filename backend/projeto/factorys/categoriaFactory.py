from projeto.models import Categoria

class CategoriaFactory:
    @staticmethod
    def criar_categoria(nome, descricao=None, id=None):
        return Categoria(nome=nome, descricao=descricao, id=id)
        