from projeto.models import Favorito, User, PontoTuristico
from . import BaseDAO

class FavoritoDAO(BaseDAO):

    def __init__(self):
        super().__init__()

    def __criar_favorito(self, linha):
        ponto = PontoTuristico(
            id=linha['id'],
            nome=linha['nome'],
            localizacao=linha['localizacao']
        )

        usuario = User(
            email=linha['email'],
            username=linha['username']
        )

        return Favorito(
            user=usuario,
            ponto_turistico=ponto
        )
    
    def adicionar_favorito(self, novo_favorito):
        sql = ''' 
            INSERT INTO favoritos (
                usuario_email,
                ponto_id
            )
            VALUES (%s, %s)
        '''
        valores = [
            novo_favorito.user.email,
            novo_favorito.ponto_turistico.id
        ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def deletar_favorito(self, usuario_email, ponto_id):
        sql = '''
            DELETE
            FROM favoritos
            WHERE usuario_email = %s AND ponto_id = %s
        '''
        valores = [
            usuario_email,
            ponto_id
        ]

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def listar_favoritos_por_usuario(self, usuario_email):
        sql = '''
            SELECT 
                u.email,
                u.username,
                p.id,
                p.nome,
                p.localizacao
            FROM favoritos AS f
            JOIN usuarios AS u ON u.email = f.usuario_email
            JOIN pontos_turisticos p ON p.id = f.ponto_id
            WHERE f.usuario_email = %s
            ORDER BY p.nome ASC;
        '''
        valor = [usuario_email]
        lista_pontos = []

        conexao = self._get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            for linha in cursor.fetchall():
                favorito = self.__criar_favorito(linha)

                lista_pontos.append(favorito)
        finally:
            cursor.close()
            conexao.close()

        return lista_pontos
    
    def verificar_favorito(self, usuario_email, ponto_id):
        sql = '''
            SELECT 1
            FROM favoritos
            WHERE usuario_email = %s AND ponto_id = %s
        '''
        valores = [usuario_email, ponto_id]
        favorito = None

        conexao = self._get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            favorito = cursor.fetchone() 
        finally:
            cursor.close()
            conexao.close()

        return favorito