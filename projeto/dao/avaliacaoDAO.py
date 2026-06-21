from projeto.factorys import UsuarioFactory, AvaliacaoFactory
from . import BaseDAO

class AvaliacaoDAO(BaseDAO):

    def __init__(self):
        super().__init__()  

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
            nova_avaliacao.ponto_id,
            nova_avaliacao.nota,
            nova_avaliacao.data_avaliacao,
            nova_avaliacao.comentario
        ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def listar_avaliacoes_por_ponto(self, ponto_id, usuario_email=None):
        sql = """
            SELECT *
            FROM vw_avaliacoes
            WHERE ponto_id = %s
        """
        
        valores = [ponto_id]

        if usuario_email:
            sql += " AND usuario_email != %s"
            valores.append(usuario_email)

        sql += """
            ORDER BY data_avaliacao DESC
        """
       
        avaliacoes_ponto = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valores)

            for linha in cursor.fetchall():
                usuario = UsuarioFactory.criar_usuario(
                    email=linha['usuario_email'],
                    username=linha['usuario_username'],
                    url_foto=linha['usuario_url_foto'],
                    tipo_usuario=linha['tipo_usuario']
                )

                avaliacao = AvaliacaoFactory.criar_avaliacao(
                    usuario=usuario,
                    ponto_id=linha['ponto_id'],
                    nota=linha['nota'],
                    data_avaliacao=linha['data_avaliacao'],
                    comentario=linha['comentario']
                )
                avaliacoes_ponto.append(avaliacao)

        finally:
            cursor.close()
            conexao.close()

        return avaliacoes_ponto

    def buscar_avaliacao(self, usuario_email, ponto_id):
        sql = """
            SELECT *
            FROM vw_avaliacoes
            WHERE usuario_email = %s AND ponto_id = %s
        """
        valor = [usuario_email, ponto_id]

        avaliacao_encontrada = None

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            linha = cursor.fetchone()

            if linha:
                usuario = UsuarioFactory.criar_usuario(
                    email=linha['usuario_email'],
                    username=linha['usuario_username'],
                    url_foto=linha['usuario_url_foto'],
                    tipo_usuario=linha['tipo_usuario']
                )

                avaliacao_encontrada = AvaliacaoFactory.criar_avaliacao(
                    usuario=usuario,
                    ponto_id=linha['ponto_id'],
                    nota=linha['nota'],
                    data_avaliacao=linha['data_avaliacao'],
                    comentario=linha['comentario']
                )

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
            avaliacao_atualizada.ponto_id
        ]

        conexao = self._get_connection()
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
            WHERE usuario_email = %s AND ponto_id = %s
        """
        valor = [usuario_email, ponto_id]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valor)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def listar_ultimas_avaliacoes_ponto(self, ponto_id, usuario_email=None, limite=5):
        sql = """
            SELECT *
            FROM vw_avaliacoes
            WHERE ponto_id = %s
        """
        
        valores = [ponto_id]

        if usuario_email:
            sql += " AND usuario_email != %s"
            valores.append(usuario_email)

        sql += """
            ORDER BY data_avaliacao DESC
            LIMIT %s
        """
        valores.append(limite)

        avaliacoes_ponto = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valores)

            for linha in cursor.fetchall():
                usuario = UsuarioFactory.criar_usuario(
                    email=linha['usuario_email'],
                    username=linha['usuario_username'],
                    url_foto=linha['usuario_url_foto'],
                    tipo_usuario=linha['tipo_usuario']
                )

                avaliacao = AvaliacaoFactory.criar_avaliacao(
                    usuario=usuario,
                    ponto_id=linha['ponto_id'],
                    nota=linha['nota'],
                    data_avaliacao=linha['data_avaliacao'],
                    comentario=linha['comentario']
                )
                avaliacoes_ponto.append(avaliacao)

        finally:
            cursor.close()
            conexao.close()

        return avaliacoes_ponto