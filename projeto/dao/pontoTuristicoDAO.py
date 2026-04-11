from projeto.models import PontoTuristico, Categoria, Promocao
from projeto.config import Config
import mysql.connector
import os

class PontoTuristicoDAO:

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
    
    def __criar_ponto_turistico(self, linha):
        categoria = Categoria(
            id=linha['categoria_id'],
            nome=linha['categoria_nome']
        )

        media_avaliacao = float(linha['media_avaliacao']) if linha['media_avaliacao'] is not None else None

        if linha['promocao_id'] is not None:
            promocao = Promocao(
                id=linha['promocao_id'],
                titulo=linha['promocao_titulo'],
                data_inicio=linha['promocao_data_inicio'],
                descricao=linha['promocao_descricao'],
                data_fim=linha['promocao_data_fim'],
                desconto=linha['promocao_desconto']
            )
        else:
            promocao = None

        return PontoTuristico(
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
    
    def __pegar_imagem_ponto(self, id_ponto):
        sql = """
            SELECT url_imagem
            FROM pontos_turisticos
            WHERE id = %s
        """
        valor = [id_ponto]
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
    
    def listar_pontos(self):
        sql = """
            SELECT 
                p.*,
                c.id AS categoria_id,
                c.nome AS categoria_nome,
                AVG(a.nota) AS media_avaliacao,

                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao

            FROM pontos_turisticos AS p

            JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
            LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id

            GROUP BY p.id
            ORDER BY p.nome ASC
        """
        lista_pontos = []

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql)
            for linha in cursor.fetchall():
                ponto = self.__criar_ponto_turistico(linha)

                lista_pontos.append(ponto)
        finally:
            cursor.close()
            conexao.close()

        return lista_pontos
    
    def listar_top_pontos(self, limite=10):
        sql = """
            SELECT 
                p.*,
                c.id AS categoria_id,
                c.nome AS categoria_nome,
                AVG(a.nota) AS media_avaliacao,

                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao

            FROM pontos_turisticos AS p

            JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
            LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id

            GROUP BY p.id
            ORDER BY media_avaliacao DESC, p.nome ASC
            LIMIT %s
        """
        valor = [limite]
        lista_pontos = []

        conexao = self.__get_connection()
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
    
    def buscar_ponto_por_id(self, id_ponto):
        sql = """
            SELECT 
                p.*,
                c.id AS categoria_id,
                c.nome AS categoria_nome,
                AVG(a.nota) AS media_avaliacao,

                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao

            FROM pontos_turisticos AS p

            JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
            LEFT JOIN promocoes AS pr ON p.promocao_id = pr.id

            WHERE p.id = %s
            GROUP BY p.id
        """
        ponto = None
        valor = [id_ponto]

        conexao = self.__get_connection()
        cursor = conexao.cursor(dictionary=True)

        try:
            cursor.execute(sql, valor)
            linha = cursor.fetchone()
            if linha:
                ponto = self.__criar_ponto_turistico(linha)
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

        conexao = self.__get_connection()
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

        conexao = self.__get_connection()
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

        conexao = self.__get_connection()
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
                AVG(a.nota) AS media_avaliacao,
                pr.id AS promocao_id,
                pr.titulo AS promocao_titulo,
                pr.desconto AS promocao_desconto,
                pr.data_inicio AS promocao_data_inicio,
                pr.data_fim AS promocao_data_fim,
                pr.descricao AS promocao_descricao
            FROM pontos_turisticos AS p
            JOIN categorias AS c ON p.categoria_id = c.id
            LEFT JOIN avaliacoes AS a ON a.ponto_id = p.id
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

        conexao = self.__get_connection()
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