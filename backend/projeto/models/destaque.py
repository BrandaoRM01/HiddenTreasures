class Destaque:

    def __init__(self, nome, id=None):
        self.__id = id
        self.__nome = nome

    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @id.setter
    def id(self, valor):
        self.__id = valor

    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    def to_dict(self):
        return {
            'id': self.__id,
            'nome': self.__nome
        }