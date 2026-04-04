from projeto.models import Categoria
from projeto.config import Config
import mysql.connector
import os

class CategoriaDAO:

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
    
    def __criar_categoria(self, linha):
        return Categoria(
            nome=linha['nome'],
            descricao=linha['descricao'],
            id=linha['id']
        )
    
    def __deletar_imagens(self, imagens):
        for (imagem,) in imagens:
            if imagem:
                caminho = os.path.join(Config.BASE_DIR, 'static', imagem)
                if os.path.exists(caminho):
                    os.remove(caminho)
    
    def carregar_categorias(self):
        sql = """
            SELECT 
                id,
                nome,
                descricao
            FROM categorias
            ORDER BY nome ASC
        """
        lista_categorias = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                categoria = self.__criar_categoria(linha)

                lista_categorias.append(categoria)
        finally:
            cursor.close()
            conexao.close()

        return lista_categorias

    def cadastrar_categoria(self, nova_categoria):
        sql = """
            INSERT INTO categorias (
                nome,
                descricao
            )
            VALUES (%s, %s)
        """
        valores = [
            nova_categoria.nome,
            nova_categoria.descricao
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_categoria(self, id_categoria):
        sql_select = """
            SELECT url_imagem
            FROM pontos_turisticos
            WHERE categoria_id = %s
        """

        sql_delete = """
            DELETE 
            FROM categorias
            WHERE id = %s
        """

        valor = [id_categoria]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql_select, valor)
            imagens = cursor.fetchall()

            cursor.execute(sql_delete, valor)
            conexao.commit()

        finally:
            cursor.close()
            conexao.close()

        self.__deletar_imagens(imagens)

    def atualizar_categoria(self, categoria_atualizada):
        sql = """
            UPDATE categorias
            SET 
                nome = %s,
                descricao = %s
            WHERE id = %s
        """
        valores = [
            categoria_atualizada.nome,
            categoria_atualizada.descricao,
            categoria_atualizada.id
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_categoria_por_id(self, id_categoria):
        sql = """
            SELECT *
            FROM categorias
            WHERE id = %s
        """
        valor = [id_categoria]

        categoria = None

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            categoria = cursor.fetchone()
        finally:
            cursor.close()
            conexao.close()

        return categoria
    
    def pegar_nomes_categorias(self):
        sql = """
            SELECT nome
            FROM categorias
            ORDER BY nome ASC
        """
        nomes_categorias = []

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql)
            for (nome,) in cursor.fetchall():
                nomes_categorias.append(nome)
        finally:
            cursor.close()
            conexao.close()

        return nomes_categorias