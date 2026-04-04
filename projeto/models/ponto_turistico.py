from .categoria import Categoria
from .promocao import Promocao

class PontoTuristico:

    def __init__(self,  nome, localizacao, promocao: Promocao=None, categoria: Categoria=None, media_avaliacao=None, descricao=None, horario_funcionamento=None, custo_entrada=None, url_imagem=None, id=None):
        self.__url_imagem = url_imagem
        self.__nome = nome
        self.__localizacao = localizacao
        self.__media_avaliacao = media_avaliacao
        self.__descricao = descricao
        self.__horario_funcionamento = horario_funcionamento
        self.__custo_entrada = custo_entrada
        self.__categoria = categoria
        self.__promocao = promocao
        self.__id = id

    @property
    def id(self):
        return self.__id
    
    @property
    def media_avaliacao(self):
        return self.__media_avaliacao
    
    @property
    def url_imagem(self):
        return self.__url_imagem
    
    @property
    def nome(self):
        return self.__nome
    
    @property
    def localizacao(self):
        return self.__localizacao
    
    @property
    def descricao(self):
        return self.__descricao
    
    @property
    def horario_funcionamento(self):
        return self.__horario_funcionamento
    
    @property 
    def custo_entrada(self):
        return self.__custo_entrada
    
    @property 
    def categoria(self):
        return self.__categoria
    
    @property
    def promocao(self):
        return self.__promocao
    
    @media_avaliacao.setter
    def media_avaliacao(self, valor):
        self.__media_avaliacao = valor
    
    @url_imagem.setter
    def url_imagem(self, valor):
        self.__url_imagem = valor

    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    @localizacao.setter
    def localizacao(self, valor):
        self.__localizacao = valor

    @descricao.setter
    def descricao(self, valor):
        self.__descricao = valor

    @horario_funcionamento.setter
    def horario_funcionamento(self, valor):
        self.__horario_funcionamento = valor

    @custo_entrada.setter
    def custo_entrada(self, valor):
        self.__custo_entrada = valor

    @categoria.setter
    def categoria(self, valor):
        self.__categoria = valor

    @id.setter
    def id(self, valor):
        self.__id = valor

    @promocao.setter
    def promocao(self, valor):
        self.__promocao = valor

    def to_dict(self):
        return {
            'id': self.__id,
            'url_imagem': self.__url_imagem,
            'nome': self.__nome,
            'localizacao': self.__localizacao,
            'descricao': self.__descricao,
            'horario_funcionamento': self.__horario_funcionamento,
            'custo_entrada': self.__custo_entrada,
            'media_avaliacao': self.__media_avaliacao,
            'categoria': self.__categoria.to_dict(),
            'promocao': self.__promocao.to_dict() if self.__promocao else None
        }