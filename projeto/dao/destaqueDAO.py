from projeto.factorys import DestaqueFactory
from . import BaseDAO

class DestaqueDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def carregar_destaques(self):
        sql = """
            SELECT id,nome
            FROM destaques
            ORDER BY nome ASC
        """

        lista_destaques = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                destaque = DestaqueFactory.criar_destaque(
                    id=linha['id'],
                    nome=linha['nome']
                )
                lista_destaques.append(destaque)
        finally:
            cursor.close()
            conexao.close()

        return lista_destaques

    def cadastrar_destaque(self, novo_destaque):
        sql = """
            INSERT INTO destaques (nome)
            VALUES (%s)
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, [novo_destaque.nome])
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def atualizar_destaque(self, destaque_atualizado):
        sql = """
            UPDATE destaques
            SET nome = %s
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, [
                destaque_atualizado.nome,
                destaque_atualizado.id
            ])
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def remover_destaque(self, id_destaque):
        sql = """
            DELETE FROM destaques
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, [id_destaque])
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_destaque_por_id(self, id_destaque):
        sql = """
            SELECT *
            FROM destaques
            WHERE id = %s
        """

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, [id_destaque])
            destaque_dados = cursor.fetchone()

            if not destaque_dados:
                return None

            return DestaqueFactory.criar_destaque(
                id=destaque_dados['id'],
                nome=destaque_dados['nome']
            )
        finally:
            cursor.close()
            conexao.close()

    def pegar_nomes_destaques(self):
        sql = """
            SELECT nome
            FROM destaques
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