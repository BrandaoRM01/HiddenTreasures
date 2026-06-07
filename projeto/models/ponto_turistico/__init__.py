from abc import ABC, abstractmethod
from projeto.models.promocao import Promocao
from projeto.models.categoria import Categoria

class PontoTuristico(ABC):

    def __init__(self,  nome, localizacao, status, promocao: Promocao=None, categoria: Categoria=None, media_avaliacao=None, descricao=None, horario_funcionamento=None, custo_entrada=None, url_imagem=None, id=None, avaliacoes=None, destaques=None, sugerido_por=None):
        self.__url_imagem = url_imagem
        self.__status = status
        self.__nome = nome
        self.__localizacao = localizacao
        self.__media_avaliacao = media_avaliacao
        self.__descricao = descricao
        self.__horario_funcionamento = horario_funcionamento
        self.__custo_entrada = custo_entrada
        self.__categoria = categoria
        self.__promocao = promocao
        self.__avaliacoes = avaliacoes if avaliacoes is not None else []
        self.__destaques = destaques if destaques is not None else []
        self.__id = id
        self.__sugerido_por = sugerido_por
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
    
    @property
    def avaliacoes(self):
        return self.__avaliacoes
    
    @property
    def status(self):
        return self.__status
    
    @property
    def destaques(self):
        return self.__destaques
    
    @property
    def sugerido_por(self):
        return self.__sugerido_por
    
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

    @avaliacoes.setter
    def avaliacoes(self, valor):
        self.__avaliacoes = valor

    @status.setter
    def status(self, valor):
        self.__status = valor

    @destaques.setter
    def destaques(self, valor):
        self.__destaques = valor

    @sugerido_por.setter
    def sugerido_por(self, valor):
        self.__sugerido_por = valor

    def adicionar_avaliacao(self, avaliacao):
        self.__avaliacoes.append(avaliacao)

    def adicionar_destaque(self, destaque):
        self.__destaques.append(destaque)

    def possui_destaque(self, destaque_id):
        for d in self.__destaques:
            if d.id == destaque_id:
                return True
        return False

    @abstractmethod
    def tipo_ponto(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

from .pontoCultural import PontoCultural
from .pontoNatural import PontoNatural