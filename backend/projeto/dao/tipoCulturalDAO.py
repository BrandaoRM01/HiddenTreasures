from projeto.factorys import TipoCulturalFactory
from . import BaseDAO

class TipoCulturalDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def carregar_tipos_culturais(self):
        sql = """
            SELECT id,nome
            FROM tipos_culturais
            ORDER BY nome ASC
        """

        lista_tipos = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                tipo = TipoCulturalFactory.criar_tipo_cultural(
                    id=linha['id'],
                    nome=linha['nome']
                )
                lista_tipos.append(tipo)
        finally:
            cursor.close()
            conexao.close()

        return lista_tipos

    def cadastrar_tipo_cultural(self, novo_tipo):
        sql = """
            INSERT INTO tipos_culturais (nome)
            VALUES (%s)
        """

        valores = [novo_tipo.nome]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def atualizar_tipo_cultural(self, tipo_atualizado):
        sql = """
            UPDATE tipos_culturais
            SET nome = %s
            WHERE id = %s
        """

        valores = [
            tipo_atualizado.nome,
            tipo_atualizado.id
        ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_tipo_cultural(self, id_tipo):
        sql = """
            DELETE FROM tipos_culturais
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, [id_tipo])
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_tipo_por_id(self, id_tipo):
        sql = """
            SELECT *
            FROM tipos_culturais
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, [id_tipo])
            tipo_cultural_dados = cursor.fetchone()

            if not tipo_cultural_dados:
                return None
        
            return TipoCulturalFactory.criar_tipo_cultural(
                id=tipo_cultural_dados['id'],
                nome=tipo_cultural_dados['nome']
            )
        finally:
            cursor.close()
            conexao.close()

    def pegar_nomes_tipos_culturais(self):
        sql = """
            SELECT nome
            FROM tipos_culturais
            ORDER BY nome ASC
        """

        nomes = []

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql)
            for (nome,) in cursor.fetchall():
                nomes.append(nome)
        finally:
            cursor.close()
            conexao.close()

        return nomes