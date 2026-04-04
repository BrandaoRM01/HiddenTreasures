class User:

    def __init__(self, email, username, senha_hash=None, url_foto=None, tipo_usuario=None):
        self.__email = email
        self.__senha_hash = senha_hash
        self.__url_foto = url_foto
        self.__username = username
        self.__tipo_usuario = tipo_usuario

    @property
    def email(self):
        return self.__email
    
    @property
    def senha_hash(self):
        return self.__senha_hash
    
    @property
    def url_foto(self):
        return self.__url_foto
    
    @property
    def username(self):
        return self.__username
    
    @property
    def tipo_usuario(self):
        return self.__tipo_usuario
    
    @email.setter
    def email(self, valor):
        self.__email = valor

    @senha_hash.setter
    def senha_hash(self, valor):
        self.__senha_hash = valor

    @url_foto.setter
    def url_foto(self, valor):
        self.__url_foto = valor

    @username.setter
    def username(self, valor):
        self.__username = valor
 
    @tipo_usuario.setter
    def tipo_usuario(self, valor):
        self.__tipo_usuario = valor

    def to_dict(self):
        return {
            'email': self.__email,
            'senha_hash': self.__senha_hash,
            'url_foto': self.__url_foto,
            'username': self.__username,
            'tipo_usuario': self.__tipo_usuario
        }