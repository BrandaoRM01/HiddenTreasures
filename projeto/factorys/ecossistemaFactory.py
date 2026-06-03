from projeto.models import Ecossistema

class EcossistemaFactory:

    @staticmethod
    def criar_ecossistema(nome, id=None):
        return Ecossistema(nome=nome, id=id)