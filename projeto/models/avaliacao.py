from .user import User
from .ponto_turistico import PontoTuristico

class Avaliacao:

    def __init__(self, usuario: User, ponto_turistico: PontoTuristico, nota, data_avaliacao, comentario=None):
        self.__usuario = usuario
        self.__ponto_turistico = ponto_turistico
        self.__nota = nota
        self.__data_avaliacao = data_avaliacao
        self.__comentario = comentario

    @property
    def usuario(self):
        return self.__usuario
    
    @property
    def ponto_turistico(self):
        return self.__ponto_turistico

    @property
    def nota(self):
        return self.__nota

    @property
    def data_avaliacao(self):
        return self.__data_avaliacao

    @property
    def comentario(self):
        return self.__comentario
    
    @usuario.setter
    def usuario(self, valor):
        self.__usuario = valor

    @ponto_turistico.setter
    def ponto_turistico(self, valor):
        self.__ponto_turistico = valor

    @nota.setter
    def nota(self, valor):
        self.__nota = valor

    @data_avaliacao.setter
    def data_avaliacao(self, valor):
        self.__data_avaliacao = valor

    @comentario.setter
    def comentario(self, valor):
        self.__comentario = valor

    def to_dict(self):
        return {
            'usuario': self.__usuario.to_dict(),
            'ponto_turistico': self.__ponto_turistico.to_dict(),
            'nota': self.__nota,
            'data_avaliacao': self.__data_avaliacao.isoformat(),
            'comentario': self.__comentario
        }