from projeto.factorys import UsuarioFactory, AvaliacaoFactory, PontoTuristicoFactory, PromocaoFactory, CategoriaFactory, EcossistemaFactory, TipoCulturalFactory, DestaqueFactory
from projeto.models import PontoCultural, PontoNatural
from . import BaseDAO
from projeto.config import Config
import os

class PontoTuristicoDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def __criar_ponto_turistico(self, linha):
        categoria = CategoriaFactory.criar_categoria(
            id=linha['categoria_id'],
            nome=linha['categoria_nome']
        )

        media_avaliacao = self.calcular_media_avaliacao(linha['id'])

        if linha['promocao_id'] is not None:
            promocao = PromocaoFactory.criar_promocao(
                id=linha['promocao_id'],
                titulo=linha['promocao_titulo'],
                data_inicio=linha['promocao_data_inicio'],
                descricao=linha['promocao_descricao'],
                data_fim=linha['promocao_data_fim'],
                desconto=linha['promocao_desconto']
            )
        else:
            promocao = None

        if linha['tipo_ponto'] == 'cultural':
            tipo_cultural = TipoCulturalFactory.criar_tipo_cultural(
                id=linha['tipo_cultural_id'],
                nome=linha['tipo_cultural_nome']
            )
            return PontoTuristicoFactory.criar_ponto_turistico(
                id=linha['id'],
                nome=linha['nome'],
                descricao=linha['descricao'],
                localizacao=linha['localizacao'],
                custo_entrada=linha['custo_entrada'],
                horario_funcionamento=linha['horario_funcionamento'],
                url_imagem=linha['url_imagem'],
                media_avaliacao=media_avaliacao,
                categoria=categoria,
                promocao=promocao,
                tipo_ponto=linha['tipo_ponto'],
                tipo_cultural=tipo_cultural,
                ano_fundacao=linha['ano_fundacao'],
                status=linha['status'],
                sugerido_por=linha['sugerido_por']
            )
        else:
            ecossistema = EcossistemaFactory.criar_ecossistema(
                id=linha['ecossistema_id'],
                nome=linha['ecossistema_nome']
            )

            return PontoTuristicoFactory.criar_ponto_turistico(
                id=linha['id'],
                nome=linha['nome'],
                descricao=linha['descricao'],
                localizacao=linha['localizacao'],
                custo_entrada=linha['custo_entrada'],
                horario_funcionamento=linha['horario_funcionamento'],
                url_imagem=linha['url_imagem'],
                media_avaliacao=media_avaliacao,
                categoria=categoria,
                promocao=promocao,
                tipo_ponto=linha['tipo_ponto'],
                ecossistema=ecossistema,
                area_km=linha['area_km2'],
                status=linha['status'],
                sugerido_por=linha['sugerido_por']
            )
    
    def calcular_media_avaliacao(self, ponto_id):
        sql = """
            SELECT AVG(nota) AS media_avaliacao
            FROM avaliacoes
            WHERE ponto_id = %s
        """
        valor = [ponto_id]
        media_avaliacao = None

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            resultado = cursor.fetchone()
            media_avaliacao = float(resultado['media_avaliacao']) if resultado['media_avaliacao'] is not None else None 
        finally:
            cursor.close()
            conexao.close()

        return media_avaliacao

    def __pegar_imagem_ponto(self, id_ponto):
        sql = """
            SELECT url_imagem
            FROM pontos_turisticos
            WHERE id = %s
        """
        valor = [id_ponto]
        resultado = None

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            resultado = cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

        return resultado
    
    def listar_pontos(self):
        sql = """
            SELECT *
            FROM vw_pontos_turisticos
            ORDER BY nome ASC
        """
        pontos_map = {}

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                ponto_id = linha['id']
                if ponto_id not in pontos_map:
                    pontos_map[ponto_id] = self.__criar_ponto_turistico(linha)

                if linha['usuario_email'] and linha['ponto_id']:
                    usuario = UsuarioFactory.criar_usuario(email=linha['email'], username=linha['username'], url_foto=linha['url_foto'], tipo_usuario=linha['tipo_usuario'])

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )
                    if avaliacao not in pontos_map[ponto_id].avaliacoes:
                        pontos_map[ponto_id].adicionar_avaliacao(avaliacao)

                if linha['destaque_nome']:
                    destaque = DestaqueFactory.criar_destaque(
                        id=linha['destaque_id'],
                        nome=linha['destaque_nome']
                    )
                    if linha['destaque_id'] and not any(d.id == linha['destaque_id'] for d in pontos_map[ponto_id].destaques):
                        pontos_map[ponto_id].adicionar_destaque(destaque)
                
        finally:
            cursor.close()
            conexao.close()

        return list(pontos_map.values())
    
    def listar_todos_pontos(self):
        sql = """
            SELECT *
            FROM vw_pontos_turisticos
            ORDER BY status DESC, nome ASC
        """
        pontos_map = {}

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                ponto_id = linha['id']
                if ponto_id not in pontos_map:
                    pontos_map[ponto_id] = self.__criar_ponto_turistico(linha)

                if linha['usuario_email'] and linha['ponto_id']:
                    usuario = UsuarioFactory.criar_usuario(email=linha['email'], username=linha['username'], url_foto=linha['url_foto'], tipo_usuario=linha['tipo_usuario'])

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )
                    if avaliacao not in pontos_map[ponto_id].avaliacoes:
                        pontos_map[ponto_id].adicionar_avaliacao(avaliacao)

                if linha['destaque_nome']:
                    destaque = DestaqueFactory.criar_destaque(
                        id=linha['destaque_id'],
                        nome=linha['destaque_nome']
                    )
                    if linha['destaque_id'] and not any(d.id == linha['destaque_id'] for d in pontos_map[ponto_id].destaques):
                        pontos_map[ponto_id].adicionar_destaque(destaque)
                
        finally:
            cursor.close()
            conexao.close()

        return list(pontos_map.values())
    
    def listar_top_pontos(self, limite=10):
        sql = """
            SELECT *
            FROM vw_pontos_turisticos
            WHERE status = 'aprovado'
        """
        pontos_map = {}

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                ponto_id = linha['id']
                if ponto_id not in pontos_map:
                    pontos_map[ponto_id] = self.__criar_ponto_turistico(linha)

                if linha['usuario_email'] and linha['ponto_id']:
                    usuario = UsuarioFactory.criar_usuario(email=linha['email'], username=linha['username'], url_foto=linha['url_foto'], tipo_usuario=linha['tipo_usuario'])

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )
                    if avaliacao not in pontos_map[ponto_id].avaliacoes:
                        pontos_map[ponto_id].adicionar_avaliacao(avaliacao)
                
                if linha['destaque_nome']:
                    destaque = DestaqueFactory.criar_destaque(
                        id=linha['destaque_id'],
                        nome=linha['destaque_nome']
                    )
                    if linha['destaque_id'] and not any(d.id == linha['destaque_id'] for d in pontos_map[ponto_id].destaques):
                        pontos_map[ponto_id].adicionar_destaque(destaque)
            
        finally:
            cursor.close()
            conexao.close()

        pontos_ordenados = sorted(list(pontos_map.values()), key=lambda ponto: (-(ponto.media_avaliacao or 0), ponto.nome))

        return pontos_ordenados[:limite]

    def buscar_ponto_por_id(self, id_ponto):
        sql = """
            SELECT *
            FROM vw_pontos_turisticos
            WHERE id = %s
        """
        ponto = None
        valor = [id_ponto]

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            resultado = cursor.fetchall()
            for linha in resultado:
                if not ponto:
                    ponto = self.__criar_ponto_turistico(linha)

                if linha['usuario_email'] and linha['ponto_id']:
                    usuario = UsuarioFactory.criar_usuario(
                        email=linha['email'],
                        username=linha['username'],
                        url_foto=linha['url_foto'],
                        tipo_usuario=linha['tipo_usuario']
                    )

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )

                    if not any(a.usuario.email == usuario.email and a.data_avaliacao == avaliacao.data_avaliacao for a in ponto.avaliacoes):
                        ponto.adicionar_avaliacao(avaliacao)

                if linha['destaque_nome']:
                    destaque = DestaqueFactory.criar_destaque(
                        id=linha['destaque_id'],
                        nome=linha['destaque_nome']
                    )
                    if linha['destaque_id'] and not any(d.id == linha['destaque_id'] for d in ponto.destaques):
                        ponto.adicionar_destaque(destaque)

            ponto.avaliacoes.sort(key=lambda avaliacao: avaliacao.data_avaliacao,reverse=True)
        finally:
            cursor.close()
            conexao.close()

        return ponto
    
    def cadastrar_ponto(self, novo_ponto, destaques_ids):
        if isinstance(novo_ponto, PontoCultural):
            sql = """
                INSERT INTO pontos_turisticos (
                    nome,
                    localizacao,
                    descricao,
                    horario_funcionamento,
                    custo_entrada,
                    url_imagem,
                    categoria_id,
                    promocao_id,
                    tipo_ponto,
                    tipo_cultural_id,
                    ano_fundacao,
                    status,
                    sugerido_por
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = [
                novo_ponto.nome,
                novo_ponto.localizacao,
                novo_ponto.descricao,
                novo_ponto.horario_funcionamento,
                novo_ponto.custo_entrada,
                novo_ponto.url_imagem,
                novo_ponto.categoria.id,
                novo_ponto.promocao.id if novo_ponto.promocao else None,
                novo_ponto.tipo_ponto(),
                novo_ponto.tipo_cultural.id if novo_ponto.tipo_cultural else None,
                novo_ponto.ano_fundacao,
                novo_ponto.status,
                novo_ponto.sugerido_por
            ]
        else:
            sql = """
                INSERT INTO pontos_turisticos (
                    nome,
                    localizacao,
                    descricao,
                    horario_funcionamento,
                    custo_entrada,
                    url_imagem,
                    categoria_id,
                    promocao_id,
                    tipo_ponto,
                    ecossistema_id,
                    area_km2,
                    status,
                    sugerido_por
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            valores = [
                novo_ponto.nome,
                novo_ponto.localizacao,
                novo_ponto.descricao,
                novo_ponto.horario_funcionamento,
                novo_ponto.custo_entrada,
                novo_ponto.url_imagem,
                novo_ponto.categoria.id,
                novo_ponto.promocao.id if novo_ponto.promocao else None,
                novo_ponto.tipo_ponto(),
                novo_ponto.ecossistema.id if novo_ponto.ecossistema else None,
                novo_ponto.area_km,
                novo_ponto.status,
                novo_ponto.sugerido_por
            ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            novo_ponto.id = cursor.lastrowid

            self.__salvar_destaques_ponto(cursor, novo_ponto.id, destaques_ids)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def atualizar_ponto(self, ponto_atualizado, imagem_antiga, destaques_ids):
        if isinstance(ponto_atualizado, PontoCultural):
            sql = """
                UPDATE pontos_turisticos
                SET 
                    nome = %s,
                    localizacao = %s,
                    descricao = %s,
                    horario_funcionamento = %s,
                    custo_entrada = %s,
                    url_imagem = %s,
                    categoria_id = %s,
                    promocao_id = %s,
                    status = %s,
                    tipo_ponto = %s,
                    tipo_cultural_id = %s,
                    ano_fundacao = %s,
                    ecossistema_id = NULL,
                    area_km2 = NULL,
                    sugerido_por = %s
                WHERE id = %s
            """

            valores = [
                ponto_atualizado.nome,
                ponto_atualizado.localizacao,
                ponto_atualizado.descricao,
                ponto_atualizado.horario_funcionamento,
                ponto_atualizado.custo_entrada,
                ponto_atualizado.url_imagem,
                ponto_atualizado.categoria.id,
                ponto_atualizado.promocao.id if ponto_atualizado.promocao else None,
                ponto_atualizado.status,
                ponto_atualizado.tipo_ponto(),
                ponto_atualizado.tipo_cultural.id if ponto_atualizado.tipo_cultural else None,
                ponto_atualizado.ano_fundacao,
                ponto_atualizado.sugerido_por,
                ponto_atualizado.id
            ]
        else:
            sql = """
                UPDATE pontos_turisticos
                SET 
                    nome = %s,
                    localizacao = %s,
                    descricao = %s,
                    horario_funcionamento = %s,
                    custo_entrada = %s,
                    url_imagem = %s,
                    categoria_id = %s,
                    promocao_id = %s,
                    status = %s,
                    tipo_ponto = %s,
                    ecossistema_id = %s,
                    area_km2 = %s,
                    tipo_cultural_id = NULL,
                    ano_fundacao = NULL,
                    sugerido_por = %s
                WHERE id = %s
            """

            valores = [
                ponto_atualizado.nome,
                ponto_atualizado.localizacao,
                ponto_atualizado.descricao,
                ponto_atualizado.horario_funcionamento,
                ponto_atualizado.custo_entrada,
                ponto_atualizado.url_imagem,
                ponto_atualizado.categoria.id,
                ponto_atualizado.promocao.id if ponto_atualizado.promocao else None,
                ponto_atualizado.status,
                ponto_atualizado.tipo_ponto(),
                ponto_atualizado.ecossistema.id if ponto_atualizado.ecossistema else None,
                ponto_atualizado.area_km,
                ponto_atualizado.sugerido_por,
                ponto_atualizado.id
            ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            self.__atualizar_destaques_ponto(cursor, ponto_atualizado.id, destaques_ids)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def excluir_ponto(self, id_ponto):
        sql =  '''
                DELETE 
                FROM pontos_turisticos 
                WHERE id = %s
        '''
        valor = [id_ponto]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            resultado = self.__pegar_imagem_ponto(id_ponto)

            if resultado:
                url = resultado['url_imagem']
                if url != "img/default/hidden_treasures_logo.png":
                    caminho = os.path.join(Config.BASE_DIR, "static", url)
                    if os.path.exists(caminho):
                        os.remove(caminho)

            self.__remover_destaques_ponto(cursor, id_ponto)
            cursor.execute(sql, valor)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_pontos(self, escrita, filtro):
        sql = """
            SELECT *
            FROM vw_pontos_turisticos
            WHERE status = 'aprovado'
        """

        valor = [f'%{escrita}%']

        if filtro == "nome":
            sql += " and nome LIKE %s"
        elif filtro == "categoria":
            sql += " and nome LIKE %s"
        elif filtro == "localizacao":
            sql += " and localizacao LIKE %s"

        sql+= "ORDER BY nome ASC"
        pontos_map = {}

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            for linha in cursor.fetchall():
                ponto_id = linha['id']
                if ponto_id not in pontos_map:
                    pontos_map[ponto_id] = self.__criar_ponto_turistico(linha)

                if linha['usuario_email'] and linha['ponto_id']:
                    usuario = UsuarioFactory.criar_usuario(email=linha['email'], username=linha['username'], url_foto=linha['url_foto'], tipo_usuario=linha['tipo_usuario'])

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )
                    pontos_map[ponto_id].adicionar_avaliacao(avaliacao)

                if linha['destaque_nome']:
                    destaque = DestaqueFactory.criar_destaque(
                        id=linha['destaque_id'],
                        nome=linha['destaque_nome']
                    )
                    if linha['destaque_id'] and not any(d.id == linha['destaque_id'] for d in pontos_map[ponto_id].destaques):
                        pontos_map[ponto_id].adicionar_destaque(destaque)
        finally:
            cursor.close()
            conexao.close()

        return list(pontos_map.values())
    
    def listar_sugestoes_usuario(self, email_usuario):
        sql = """
            SELECT *
            FROM vw_pontos_turisticos
            WHERE sugerido_por = %s
            ORDER BY status ASC, p.nome ASC
        """
        pontos_map = {}
        valor = [email_usuario]

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            for linha in cursor.fetchall():
                ponto_id = linha['id']
                if ponto_id not in pontos_map:
                    pontos_map[ponto_id] = self.__criar_ponto_turistico(linha)

                if linha['usuario_email'] and linha['ponto_id']:
                    usuario = UsuarioFactory.criar_usuario(email=linha['email'], username=linha['username'], url_foto=linha['url_foto'], tipo_usuario=linha['tipo_usuario'])

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )
                    if avaliacao not in pontos_map[ponto_id].avaliacoes:
                        pontos_map[ponto_id].adicionar_avaliacao(avaliacao)

                if linha['destaque_nome']:
                    destaque = DestaqueFactory.criar_destaque(
                        id=linha['destaque_id'],
                        nome=linha['destaque_nome']
                    )
                    if linha['destaque_id'] and not any(d.id == linha['destaque_id'] for d in pontos_map[ponto_id].destaques):
                        pontos_map[ponto_id].adicionar_destaque(destaque)   
        finally:
            cursor.close()
            conexao.close()

        return list(pontos_map.values())
    
    def listar_pontos_sugeridos(self):
        sql = """
            SELECT *
            FROM vw_pontos_turisticos
            WHERE sugerido_por IS NOT NULL
            ORDER BY status ASC, p.nome ASC
        """
        pontos_map = {}

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                ponto_id = linha['id']
                if ponto_id not in pontos_map:
                    pontos_map[ponto_id] = self.__criar_ponto_turistico(linha)

                if linha['usuario_email'] and linha['ponto_id']:
                    usuario = UsuarioFactory.criar_usuario(email=linha['email'], username=linha['username'], url_foto=linha['url_foto'], tipo_usuario=linha['tipo_usuario'])

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )
                    if avaliacao not in pontos_map[ponto_id].avaliacoes:
                        pontos_map[ponto_id].adicionar_avaliacao(avaliacao)

                if linha['destaque_nome']:
                    destaque = DestaqueFactory.criar_destaque(
                        id=linha['destaque_id'],
                        nome=linha['destaque_nome']
                    )
                    if linha['destaque_id'] and not any(d.id == linha['destaque_id'] for d in pontos_map[ponto_id].destaques):
                        pontos_map[ponto_id].adicionar_destaque(destaque)   
        finally:
            cursor.close()
            conexao.close()

        return list(pontos_map.values())
    
    def alterar_status(self, id_ponto, status):
        sql = """
            UPDATE pontos_turisticos
            SET status = %s
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, (status, id_ponto))
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def __salvar_destaques_ponto(self, cursor, id_ponto, destaques_ids):
        for id in destaques_ids:
            sql = """
                INSERT INTO pontos_destaques (ponto_id, destaque_id)
                VALUES (%s, %s)
            """
            valores = [id_ponto, id]
            cursor.execute(sql, valores)

    def __remover_destaques_ponto(self, cursor, id_ponto):
        sql = """
            DELETE FROM pontos_destaques
            WHERE ponto_id = %s
        """
        valor = [id_ponto]
        cursor.execute(sql, valor)

    def __atualizar_destaques_ponto(self, cursor, id_ponto, destaques_ids):
        self.__remover_destaques_ponto(cursor, id_ponto)
        self.__salvar_destaques_ponto(cursor, id_ponto, destaques_ids)