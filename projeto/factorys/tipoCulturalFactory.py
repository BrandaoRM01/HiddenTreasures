from projeto.models import TipoCultural

class TipoCulturalFactory:

    @staticmethod
    def criar_tipo_cultural(nome, id=None):
        return TipoCultural(nome=nome, id=id)