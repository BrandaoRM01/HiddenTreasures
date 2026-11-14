from projeto.models import Promocao

class PromocaoFactory:

    @staticmethod
    def criar_promocao(titulo, desconto, data_inicio, data_fim, id=None, descricao=None):
        return Promocao(
            titulo=titulo,
            desconto=desconto,
            data_inicio=data_inicio,
            data_fim=data_fim,
            id=id,
            descricao=descricao
        )