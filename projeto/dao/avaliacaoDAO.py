from projeto.models import Avaliacao, User, PontoTuristico
from projeto.config import Config
import mysql.connector

class AvaliacaoDAO:

    def __init__(self):
        self.__db_config = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DATABASE,
            'port': Config.MYSQL_PORT
        }

    def __get_connection(self):
        return mysql.connector.connect(**self.__db_config)
    
    def __criar_avaliacao(self, linha):
        usuario = User(
            email=linha['usuario_email'],
            username=linha['usuario_username'],
            url_foto=linha['usuario_url_foto']
        )

        ponto_turistico = PontoTuristico(
            id=linha['ponto_id'],
            nome=linha['ponto_nome'],
            localizacao=linha['ponto_localizacao']
        )

        return Avaliacao(
            usuario=usuario,
            ponto_turistico=ponto_turistico,
            nota=linha['nota'],
            data_avaliacao=linha['data_avaliacao'],
            comentario=linha['comentario']
        )
   
    def cadastrar_avaliacao(self, nova_avaliacao):
        sql = """
            INSERT INTO avaliacoes (
                usuario_email,
                ponto_id,
                nota,
                data_avaliacao,
                comentario
            )
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = [
            nova_avaliacao.usuario.email,
            nova_avaliacao.ponto_turistico.id,
            nova_avaliacao.nota,
            nova_avaliacao.data_avaliacao,
            nova_avaliacao.comentario
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def listar_avaliacoes_por_ponto(self, ponto_id, usuario_email=None):
        sql = """
            SELECT 
                a.*,
                u.email AS usuario_email,
                u.username AS usuario_username,
                u.url_foto AS usuario_url_foto,
                p.id AS ponto_id,
                p.nome AS ponto_nome,
                p.localizacao AS ponto_localizacao
            FROM avaliacoes AS a
            JOIN usuarios AS u ON a.usuario_email = u.email
            JOIN pontos_turisticos AS p ON a.ponto_id = p.id
            WHERE a.ponto_id = %s
        """
        
        valores = [ponto_id]

        if usuario_email:
            sql += " AND a.usuario_email != %s"
            valores.append(usuario_email)

        sql += """
            ORDER BY a.data_avaliacao DESC
        """
       
        avaliacoes_ponto = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valores)

            for linha in cursor.fetchall():
                avaliacao = self.__criar_avaliacao(linha)
                avaliacoes_ponto.append(avaliacao)

        finally:
            cursor.close()
            conexao.close()

        return avaliacoes_ponto

    def buscar_avaliacao(self, usuario_email, ponto_id):
        sql = """
            SELECT 
                a.*,
                u.email AS usuario_email,
                u.username AS usuario_username,
                u.url_foto AS usuario_url_foto,
                p.id AS ponto_id,
                p.nome AS ponto_nome,
                p.localizacao AS ponto_localizacao
            FROM avaliacoes AS a
            JOIN usuarios AS u ON a.usuario_email = u.email
            JOIN pontos_turisticos AS p ON a.ponto_id = p.id
            WHERE a.usuario_email = %s AND a.ponto_id = %s
        """
        valor = [usuario_email, ponto_id]

        avaliacao_encontrada = None

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            linha = cursor.fetchone()

            if linha:
                avaliacao_encontrada = self.__criar_avaliacao(linha)

        finally:
            cursor.close()
            conexao.close()

        return avaliacao_encontrada
    
    def atualizar_avaliacao(self, avaliacao_atualizada):
        sql = """
            UPDATE avaliacoes
            SET 
                nota = %s,
                comentario = %s,
                data_avaliacao = %s
            WHERE usuario_email = %s AND ponto_id = %s
        """
        valores = [
            avaliacao_atualizada.nota,
            avaliacao_atualizada.comentario,
            avaliacao_atualizada.data_avaliacao,
            avaliacao_atualizada.usuario.email,
            avaliacao_atualizada.ponto_turistico.id
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()
        
    def remover_avaliacao(self, usuario_email, ponto_id):
        sql = """
            DELETE 
            FROM avaliacoes
            WHERE usuario_email = %sAND ponto_id = %s
        """
        valor = [usuario_email, ponto_id]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valor)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def listar_ultimas_avaliacoes_ponto(self, ponto_id, usuario_email=None, limite=5):
        sql = """
            SELECT 
                a.*,
                u.email AS usuario_email,
                u.username AS usuario_username,
                u.url_foto AS usuario_url_foto,
                p.id AS ponto_id,
                p.nome AS ponto_nome,
                p.localizacao AS ponto_localizacao
            FROM avaliacoes AS a
            JOIN usuarios AS u ON a.usuario_email = u.email
            JOIN pontos_turisticos AS p ON a.ponto_id = p.id
            WHERE a.ponto_id = %s
        """
        
        valores = [ponto_id]

        if usuario_email:
            sql += " AND a.usuario_email != %s"
            valores.append(usuario_email)

        sql += """
            ORDER BY a.data_avaliacao DESC
            LIMIT %s
        """
        valores.append(limite)

        avaliacoes_ponto = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valores)

            for linha in cursor.fetchall():
                avaliacao = self.__criar_avaliacao(linha)
                avaliacoes_ponto.append(avaliacao)

        finally:
            cursor.close()
            conexao.close()

        return avaliacoes_ponto