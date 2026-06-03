from projeto.factorys import EcossistemaFactory
from . import BaseDAO

class EcossistemaDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def carregar_ecossistemas(self):
        sql = """
            SELECT id,nome
            FROM ecossistemas
            ORDER BY nome ASC
        """

        lista_ecossistemas = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                eco = EcossistemaFactory.criar_ecossistema(
                    id=linha['id'],
                    nome=linha['nome']
                )
                lista_ecossistemas.append(eco)
        finally:
            cursor.close()
            conexao.close()

        return lista_ecossistemas

    def cadastrar_ecossistema(self, novo_ecossistema):
        sql = """
            INSERT INTO ecossistemas (nome)
            VALUES (%s)
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, [novo_ecossistema.nome])
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def atualizar_ecossistema(self, ecossistema_atualizado):
        sql = """
            UPDATE ecossistemas
            SET nome = %s
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, [
                ecossistema_atualizado.nome,
                ecossistema_atualizado.id
            ])
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_ecossistema(self, id_ecossistema):
        sql = """
            DELETE FROM ecossistemas
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, [id_ecossistema])
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_ecossistema_por_id(self, id_ecossistema):
        sql = """
            SELECT *
            FROM ecossistemas
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, [id_ecossistema])
            ecossistema_dados = cursor.fetchone()
            return EcossistemaFactory.criar_ecossistema(
                id=ecossistema_dados['id'],
                nome=ecossistema_dados['nome']
            )
        finally:
            cursor.close()
            conexao.close()

    def pegar_nomes_ecossistemas(self):
        sql = """
            SELECT nome
            FROM ecossistemas
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