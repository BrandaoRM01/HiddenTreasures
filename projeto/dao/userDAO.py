from projeto.models import User
from projeto.config import Config
import mysql.connector
from werkzeug.security import generate_password_hash
import os

class UserDAO:

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
    
    def __criar_usuario(self, linha):
        return User(
            email=linha['email'],
            senha_hash=linha['senha_hash'],
            url_foto=linha['url_foto'],
            username=linha['username'],
            tipo_usuario=linha['tipo_usuario']
        )
    
    def __pegar_foto_usuario(self, email):
        sql = """
            SELECT url_foto
            FROM usuarios
            WHERE email = %s
        """
        valor = [email]

        resultado = None

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            resultado = cursor.fetchone()

        finally:
            cursor.close()
            conexao.close()

        return resultado
    
    def criar_usuario_superadmin(self):
        superadmin_email = Config.SUPERADMIN_EMAIL
        superadmin_senha = Config.SUPERADMIN_PASSWORD
        superadmin_username = Config.SUPERADMIN_USERNAME

        usuario = self.buscar_usuario_por_email(superadmin_email)

        if not usuario:
            senha_hash = generate_password_hash(superadmin_senha)

            superadmin = User(
                email=superadmin_email,
                senha_hash=senha_hash,
                url_foto="img/default/user_foto.webp",
                username=superadmin_username.capitalize().strip(),
                tipo_usuario="superadmin"
            )

            self.cadastrar_usuario(superadmin)
    
    def cadastrar_usuario(self, novo_usuario):
        sql = """
            INSERT INTO usuarios (
                email,
                senha_hash,
                url_foto,
                username,
                tipo_usuario
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        if not novo_usuario.tipo_usuario:
            novo_usuario.tipo_usuario = 'user'

        valores = [
            novo_usuario.email,
            novo_usuario.senha_hash,
            novo_usuario.url_foto,
            novo_usuario.username,
            novo_usuario.tipo_usuario
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def buscar_usuario_por_email(self, email):
        sql = """
            SELECT *
            FROM usuarios
            WHERE email = %s
        """
        valor = [email]

        usuario_encontrado = None

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            resultado = cursor.fetchone()

            if resultado:
                usuario_encontrado = self.__criar_usuario(resultado)
             
        finally:
            cursor.close()
            conexao.close()

        return usuario_encontrado
    
    def listar_usuarios(self):
        sql = """
            SELECT *
            FROM usuarios
            ORDER BY tipo_usuario DESC, email ASC
        """
        lista_usuarios = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                usuario = self.__criar_usuario(linha)

                lista_usuarios.append(usuario)
        finally:
            cursor.close()
            conexao.close()

        return lista_usuarios
    
    def excluir_usuario(self, email):
        sql = """
            DELETE 
            FROM usuarios
            WHERE email = %s
        """
        valor = [email]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            resultado = self.__pegar_foto_usuario(email)

            if resultado:
                url_foto = resultado['url_foto']

                if url_foto != "img/default/user_foto.webp":

                    caminho_foto = os.path.join(Config.BASE_DIR, "static", url_foto)

                    if os.path.exists(caminho_foto):
                        os.remove(caminho_foto)

            cursor.execute(sql, valor)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def pegar_usernames(self):
        sql = """
            SELECT username
            FROM usuarios
        """
        lista_usernames = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                username = linha['username']

                lista_usernames.append(username)
        finally:
            cursor.close()
            conexao.close()

        return lista_usernames
    
    def alterar_permissao_usuario(self, usuario_atualizado):
        sql = '''
            UPDATE usuarios
            SET tipo_usuario = %s
            WHERE email = %s
        '''
        valores = [
            usuario_atualizado.tipo_usuario,
            usuario_atualizado.email
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

    def editar_usuario(self, usuario_atualizado, imagem_antiga):
        sql = '''
            UPDATE usuarios
            SET 
                username = %s,
                senha_hash = %s,
                url_foto = %s
            WHERE email = %s
        '''
        valores = [
            usuario_atualizado.username,
            usuario_atualizado.senha_hash,
            usuario_atualizado.url_foto,
            usuario_atualizado.email
        ]

        conexao = self.__get_connection()
        cursor = conexao.cursor()

        try:
            cursor.execute(sql, valores)
            conexao.commit()
        finally:
            cursor.close()
            conexao.close()

        if imagem_antiga != usuario_atualizado.url_foto:
            if imagem_antiga != "img/default/user_foto.webp":
                caminho = os.path.join(Config.BASE_DIR, "static", imagem_antiga)
                if os.path.exists(caminho):
                    os.remove(caminho)