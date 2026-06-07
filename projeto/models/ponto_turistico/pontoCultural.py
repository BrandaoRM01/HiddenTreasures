from . import PontoTuristico
from projeto.models.tipo_cultural import TipoCultural

class PontoCultural(PontoTuristico):

    def __init__(self,  nome, localizacao, tipo_cultural, status, ano_fundacao=None, promocao=None, categoria=None, media_avaliacao=None, descricao=None, horario_funcionamento=None, custo_entrada=None, url_imagem=None, id=None, avaliacoes=None, destaques=None, sugerido_por=None):
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
                destaques=destaques,
                sugerido_por=sugerido_por   
        )
        self.__tipo_cultural = tipo_cultural
        self.__ano_fundacao = ano_fundacao

    @property
    def tipo_cultural(self):
        return self.__tipo_cultural

    @property
    def ano_fundacao(self):
        return self.__ano_fundacao
    
    @tipo_cultural.setter
    def tipo_cultural(self, valor):
        self.__tipo_cultural = valor
    
    @ano_fundacao.setter
    def ano_fundacao(self, valor):
        self.__ano_fundacao = valor

    def tipo_ponto(self):
        return "cultural"

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
            'tipo_cultural': self.__tipo_cultural.to_dict(),
            'ano_fundacao': self.__ano_fundacao if self.__ano_fundacao else 'Não Informado',
            'tipo_ponto': self.tipo_ponto(),
            'status': self.status,
            'destaques': [destaque.to_dict() for destaque in self.destaques],
            'sugerido_por': self.sugerido_por if self.sugerido_por else None
        }