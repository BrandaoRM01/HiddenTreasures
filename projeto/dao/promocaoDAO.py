from projeto.models import Promocao
from projeto.config import Config
import mysql.connector

class PromocaoDAO:  

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
    
    def __criar_promocao(self, linha):
        return Promocao(
            id=linha['id'],
            titulo=linha['titulo'],
            descricao=linha['descricao'],
            desconto=linha['desconto'],
            data_inicio=linha['data_inicio'],
            data_fim=linha['data_fim']
        )
    
    def cadastrar_promocao(self, nova_promocao):
        sql = """
            INSERT INTO promocoes (
                titulo,
                descricao,
                desconto,
                data_inicio,
                data_fim
            )
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = [
            nova_promocao.titulo,
            nova_promocao.descricao,
            nova_promocao.desconto,
            nova_promocao.data_inicio,
            nova_promocao.data_fim
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def listar_promocoes_ativas(self):
        sql = """
            SELECT 
                id,
                titulo,
                descricao,
                desconto,
                data_inicio,
                data_fim
            FROM promocoes
            WHERE (data_inicio IS NULL OR data_inicio <= CURDATE())AND (data_fim IS NULL OR data_fim >= CURDATE())
            ORDER BY data_inicio DESC
        """
        lista_promocoes = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                promocao = self.__criar_promocao(linha)

                lista_promocoes.append(promocao)
        finally:
            cursor.close()
            conexao.close()

        return lista_promocoes
    
    def listar_todas_promocoes(self):
        sql = """
            SELECT 
                id,
                titulo,
                descricao,
                desconto,
                data_inicio,
                data_fim
            FROM promocoes
            ORDER BY data_inicio DESC
        """
        lista_promocoes = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                promocao = self.__criar_promocao(linha)

                lista_promocoes.append(promocao)
        finally:
            cursor.close()
            conexao.close()

        return lista_promocoes
    
    def pegar_promocao_por_id(self, promocao_id):
        sql = """
            SELECT 
                id,
                titulo,
                descricao,
                desconto,
                data_inicio,
                data_fim
            FROM promocoes
            WHERE id = %s
        """
        valor = [promocao_id]
        promocao_encontrada = None

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            promocao_encontrada = cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

        return promocao_encontrada
    
    def deletar_promocao(self, promocao_id):
        sql = """
            DELETE 
            FROM promocoes
            WHERE id = %s
        """
        valor = [promocao_id]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valor)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def atualizar_promocao(self, promocao_atualizada):
        sql = """
            UPDATE promocoes
            SET 
                titulo = %s,
                descricao = %s,
                desconto = %s,
                data_inicio = %s,
                data_fim = %s
            WHERE id = %s
        """
        valores = [
            promocao_atualizada.titulo,
            promocao_atualizada.descricao,
            promocao_atualizada.desconto,
            promocao_atualizada.data_inicio,
            promocao_atualizada.data_fim,
            promocao_atualizada.id
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def deletar_promocoes_expiradas(self):
        sql = """
            DELETE 
            FROM promocoes
            WHERE data_fim < CURDATE()
        """

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_promocao_por_titulo(self, titulo):
        sql = """
            SELECT 
                id,
                titulo,
                descricao,
                desconto,
                data_inicio,
                data_fim
            FROM promocoes
            WHERE titulo = %s
        """
        valor = [titulo]
        promocao_encontrada = None

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            linha = cursor.fetchone()

            if linha:
                promocao_encontrada = self.__criar_promocao(linha)

        finally:
            cursor.close()
            conexao.close()

        return promocao_encontrada