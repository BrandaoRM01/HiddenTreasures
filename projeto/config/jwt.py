import jwt
from datetime import datetime, timedelta, timezone
from projeto.config import Config

class JWT:
    
    @staticmethod
    def gerar_token(usuario):
        payload = {
            'email': usuario.email,
            'tipo_usuario': usuario.tipo_usuario(),
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)
        }

        return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

    @staticmethod
    def decodificar_token(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None