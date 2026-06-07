from . import PontoTuristico
from projeto.models.ecossistema import Ecossistema

class PontoNatural(PontoTuristico):

    def __init__(self,  nome, localizacao, ecossistema, status, area_km=None, promocao=None, categoria=None, media_avaliacao=None, descricao=None, horario_funcionamento=None, custo_entrada=None, url_imagem=None, id=None, avaliacoes=None, destaques=None):
        super().__init__(
            nome=nome,
            localizacao=localizacao,
            status=status,
            promocao=promocao,
            categoria=categoria,
            media_avaliacao=media_avaliacao,
            descricao=descricao,
            horario_funcionamento=horario_funcionamento,
            custo_entrada=custo_entrada,
            url_imagem=url_imagem,
            id=id,
            avaliacoes=avaliacoes,
            destaques=destaques
        )
        self.__ecossistema = ecossistema
        self.__area_km = area_km

    @property
    def ecossistema(self):
        return self.__ecossistema

    @property
    def area_km(self):
        return self.__area_km
    
    @ecossistema.setter
    def ecossistema(self, valor):
        self.__ecossistema = valor
    
    @area_km.setter
    def area_km(self, valor):
        self.__area_km = valor

    def tipo_ponto(self):
        return "natural"

    def to_dict(self):
        return {
            'id': self.id,
            'url_imagem': self.url_imagem,
            'nome': self.nome,
            'localizacao': self.localizacao,
            'descricao': self.descricao,
            'horario_funcionamento': self.horario_funcionamento,
            'custo_entrada': self.custo_entrada,
            'media_avaliacao': self.media_avaliacao,
            'categoria': self.categoria.to_dict(),
            'promocao': self.promocao.to_dict() if self.promocao else None,
            'avaliacoes': [avaliacao.to_dict() for avaliacao in self.avaliacoes],
            'ecossistema': self.__ecossistema.to_dict(),
            'area_km': self.__area_km if self.__area_km else 0,
            'tipo_ponto': self.tipo_ponto(),
            'status': self.status,
            'destaques': [destaque.to_dict() for destaque in self.destaques]
        }