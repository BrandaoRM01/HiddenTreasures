class Categoria:

    def __init__(self, nome, descricao=None, id=None):
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, valor):
        self.__id = valor
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def descricao(self):
        return self.__descricao
    
    @nome.setter
    def nome(self, valor):
        self.__nome = valor
    
    @descricao.setter
    def descricao(self, valor):
        self.__descricao = valor

    def to_dict(self):
        return {
            'id': self.__id,
            'nome': self.__nome,
            'descricao': self.__descricao
        }