from .user import User

class HistoricoSenha:
    def __init__(self, usuario: User, senha_hash, criado_em=None):
        self.__usuario = usuario         
        self.__senha_hash = senha_hash
        self.__criado_em = criado_em

    @property
    def usuario(self):
        return self.__usuario
    
    @property
    def senha_hash(self):
        return self.__senha_hash
    
    @property
    def criado_em(self):
        return self.__criado_em
    
    @usuario.setter
    def usuario(self, valor):
        self.__usuario = valor

    @senha_hash.setter
    def senha_hash(self, valor):
        self.__senha_hash = valor

    @criado_em.setter
    def criado_em(self, valor):
        self.__criado_em = valor

    def to_dict(self):
        return {
            'usuario': self.__usuario.to_dict(),
            'senha_hash': self.__senha_hash,
            'criado_em': self.__criado_em
        }