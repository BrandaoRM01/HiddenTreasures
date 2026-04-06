from .ponto_turistico import PontoTuristico
from .user import User

class Favorito:

    def __init__(self, user:User, ponto_turistico:PontoTuristico):
        self.__user = user
        self.__ponto_turistico = ponto_turistico

    @property
    def user(self):
        return self.__user
    
    @property
    def ponto_turistico(self):
        return self.__ponto_turistico
    
    @user.setter
    def user(self, valor):
        self.__user = valor

    @ponto_turistico.setter
    def ponto_turistico(self, valor):
        self.__ponto_turistico = valor

    def to_dict(self):
        return {
            'user': self.__user.to_dict(),
            'ponto_turistico': self.__ponto_turistico.to_dict()
        }