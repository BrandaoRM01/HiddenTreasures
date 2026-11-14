from projeto.models import PontoNatural, PontoCultural, Categoria, Promocao

class PontoTuristicoFactory:

    @staticmethod
    def criar_ponto_turistico(tipo_ponto, nome, localizacao, status, promocao: Promocao=None, categoria: Categoria=None, media_avaliacao=None, descricao=None, horario_funcionamento=None, custo_entrada=None, url_imagem=None, id=None, avaliacoes=None, tipo_cultural=None, ano_fundacao=None, ecossistema=None, area_km=None, destaques=None, sugerido_por=None):
        if tipo_ponto == "cultural":
            return PontoCultural(
                nome=nome,
                localizacao=localizacao,
                status=status,
                tipo_cultural=tipo_cultural,
                ano_fundacao=ano_fundacao,
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
        else:
            return PontoNatural(
                nome=nome,
                localizacao=localizacao,
                status=status,
                ecossistema=ecossistema,
                area_km=area_km,
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