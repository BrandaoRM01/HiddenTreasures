from projeto.models import PontoTuristico, Categoria, Promocao

class PontoTuristicoFactory:

    @staticmethod
    def criar_ponto_turistico(nome, localizacao, promocao: Promocao=None, categoria: Categoria=None, media_avaliacao=None, descricao=None, horario_funcionamento=None, custo_entrada=None, url_imagem=None, id=None, avaliacoes=None):
        return PontoTuristico(
            nome=nome,
            localizacao=localizacao,
            promocao=promocao,
            categoria=categoria,
            media_avaliacao=media_avaliacao,
            descricao=descricao,
            horario_funcionamento=horario_funcionamento,
            custo_entrada=custo_entrada,
            url_imagem=url_imagem,
            id=id,
            avaliacoes=avaliacoes
        )