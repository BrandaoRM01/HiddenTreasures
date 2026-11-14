class Promocao:

    def __init__(self, titulo, desconto, data_inicio, data_fim, id=None, descricao=None):
        self.__id = id
        self.__titulo = titulo
        self.__descricao = descricao
        self.__desconto = desconto
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim

    @property
    def id(self):
        return self.__id
    
    @property
    def titulo(self):
        return self.__titulo
    
    @property
    def descricao(self):
        return self.__descricao
    
    @property
    def desconto(self):
        return self.__desconto
    
    @property
    def data_inicio(self):
        return self.__data_inicio
    
    @property
    def data_fim(self):
        return self.__data_fim
    
    @id.setter
    def id(self, valor):
        self.__id = valor

    @titulo.setter
    def titulo(self, valor):
        self.__titulo = valor

    @descricao.setter
    def descricao(self, valor):
        self.__descricao = valor

    @desconto.setter
    def desconto(self, valor):
        self.__desconto = valor

    @data_inicio.setter
    def data_inicio(self, valor):
        self.__data_inicio = valor

    @data_fim.setter
    def data_fim(self, valor):
        self.__data_fim = valor

    def to_dict(self):
        return {
            'id': self.__id,
            'titulo': self.__titulo,
            'descricao': self.__descricao,
            'desconto': self.__desconto,
            'data_inicio': self.__data_inicio.isoformat(),
            'data_fim': self.__data_fim.isoformat()
        }