
from projeto.models import Avaliacao, Usuario

class AvaliacaoFactory:

    @staticmethod
    def criar_avaliacao(usuario: Usuario, ponto_id, nota, data_avaliacao, comentario):
        return Avaliacao(
            usuario=usuario,
            ponto_id=ponto_id,
            nota=nota,
            data_avaliacao=data_avaliacao,
            comentario=comentario
        )