from projeto.models import PontoTuristico, Categoria, Promocao
from projeto.factorys import UsuarioFactory, AvaliacaoFactory, PontoTuristicoFactory, PromocaoFactory, CategoriaFactory
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
            promocao=promocao
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
            SELECT 
                p.*,
                c.id AS categoria_id,
                c.nome AS categoria_nome,

                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao,

                a.ponto_id,
                a.usuario_email,
                a.nota,
                a.data_avaliacao,
                a.comentario,

                u.email,
                u.username,
                u.url_foto,
                u.tipo_usuario

            FROM pontos_turisticos AS p

            INNER JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
            LEFT JOIN usuarios AS u ON a.usuario_email = u.email
            LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id

            ORDER BY p.nome ASC
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
                
        finally:
            cursor.close()
            conexao.close()

        return list(pontos_map.values())
    
    def listar_top_pontos(self, limite=10):
        sql = """
            SELECT 
                p.*,
                c.id AS categoria_id,
                c.nome AS categoria_nome,

                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao,

                a.ponto_id,
                a.usuario_email,
                a.nota,
                a.data_avaliacao,
                a.comentario,

                u.email,
                u.username,
                u.url_foto,
                u.tipo_usuario

            FROM pontos_turisticos AS p

            INNER JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
            LEFT JOIN usuarios AS u ON a.usuario_email = u.email
            LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id

            LIMIT %s
        """
        valor = [limite]
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
                    if avaliacao not in pontos_map[ponto_id].avaliacoes:
                        pontos_map[ponto_id].adicionar_avaliacao(avaliacao)
            
        finally:
            cursor.close()
            conexao.close()

        return sorted(list(pontos_map.values()), key=lambda ponto: (-(ponto.media_avaliacao or 0), ponto.nome))

    def buscar_ponto_por_id(self, id_ponto):
        sql = """
            SELECT 
                p.*,
                c.id AS categoria_id,
                c.nome AS categoria_nome,

                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao,

                a.ponto_id,
                a.usuario_email,
                a.nota,
                a.data_avaliacao,
                a.comentario,

                u.email,
                u.username,
                u.url_foto,
                u.tipo_usuario

            FROM pontos_turisticos AS p

            INNER JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
            LEFT JOIN usuarios AS u ON a.usuario_email = u.email
            LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id

            WHERE p.id = %s
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
                    usuario = UsuarioFactory.criar_usuario(email=linha['email'], username=linha['username'], url_foto=linha['url_foto'], tipo_usuario=linha['tipo_usuario'])

                    avaliacao = AvaliacaoFactory.criar_avaliacao(
                        usuario=usuario,
                        ponto_id=linha['ponto_id'],
                        nota=linha['nota'],
                        data_avaliacao=linha['data_avaliacao'],
                        comentario=linha['comentario']
                    )
                    if avaliacao not in ponto.avaliacoes:
                        ponto.adicionar_avaliacao(avaliacao)
            ponto.avaliacoes.sort(key=lambda avaliacao: avaliacao.data_avaliacao,reverse=True)
        finally:
            cursor.close()
            conexao.close()

        return ponto
    
    def cadastrar_ponto(self, novo_ponto):
        sql = """
            INSERT INTO pontos_turisticos (
                nome,
                localizacao,
                descricao,
                horario_funcionamento,
                custo_entrada,
                url_imagem,
                categoria_id,
                promocao_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = [
            novo_ponto.nome,
            novo_ponto.localizacao,
            novo_ponto.descricao,
            novo_ponto.horario_funcionamento,
            novo_ponto.custo_entrada,
            novo_ponto.url_imagem,
            novo_ponto.categoria.id,
            novo_ponto.promocao.id if novo_ponto.promocao else None
        ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def atualizar_ponto(self, ponto_atualizado, imagem_antiga):
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
                promocao_id = %s
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
            ponto_atualizado.id
        ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
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

            cursor.execute(sql, valor)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_pontos(self, escrita, filtro):
        sql = """
            SELECT 
                p.*,
                c.id AS categoria_id,
                c.nome AS categoria_nome,
                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao
            FROM pontos_turisticos AS p
            INNER JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id
        """

        valor = [f'%{escrita}%']

        if filtro == "nome":
            sql += "WHERE p.nome LIKE %s"
        elif filtro == "categoria":
            sql += "WHERE c.nome LIKE %s"
        elif filtro == "localizacao":
            sql += "WHERE p.localizacao LIKE %s"

        sql+= " GROUP BY p.id ORDER BY p.nome ASC"
        lista_pontos = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            for linha in cursor.fetchall():
                ponto = self.__criar_ponto_turistico(linha)

                lista_pontos.append(ponto)
        finally:
            cursor.close()
            conexao.close()

        return lista_pontos