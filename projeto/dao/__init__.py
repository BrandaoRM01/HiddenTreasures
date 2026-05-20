from projeto.config import Config
import mysql.connector

class BaseDAO:
    def __init__(self):
        self.__db_config = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DATABASE,
            'port': Config.MYSQL_PORT
        }

    def _get_connection(self):
        return mysql.connector.connect(**self.__db_config)
    
from .categoriaDAO import CategoriaDAO
from .pontoTuristicoDAO import PontoTuristicoDAO
from .userDAO import UserDAO
from .avaliacaoDAO import AvaliacaoDAO
from .promocaoDAO import PromocaoDAO
from .favoritoDAO import FavoritoDAO
from .historicoSenhaDAO import HistoricoSenhaDAO