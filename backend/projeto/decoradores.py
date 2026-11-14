from functools import wraps
from flask import request, jsonify
from projeto.config import JWT
from projeto.dao import UserDAO

def __extrair_usuario_do_token():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    payload = JWT.decodificar_token(token)

    if not payload:
        return None

    dao_usuario = UserDAO()
    usuario = dao_usuario.buscar_usuario_por_email(payload['email'])

    return usuario


def login_required(f):
    @wraps(f)
    def decorada(self, *args, **kwargs):
        usuario = __extrair_usuario_do_token()

        if not usuario:
            return jsonify({'mensagem': 'você precisa estar logado', 'classe': 'danger'}), 401

        return f(self, usuario, *args, **kwargs)
    return decorada


def admin_required(f):
    @wraps(f)
    def decorada(self, *args, **kwargs):
        usuario = __extrair_usuario_do_token()

        if not usuario:
            return jsonify({'mensagem': 'você precisa estar logado', 'classe': 'danger'}), 401

        if usuario.tipo_usuario() not in ['admin', 'superadmin']:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        return f(self, usuario, *args, **kwargs)
    return decorada


def superadmin_required(f):
    @wraps(f)
    def decorada(self, *args, **kwargs):
        usuario = __extrair_usuario_do_token()

        if not usuario:
            return jsonify({'mensagem': 'você precisa estar logado', 'classe': 'danger'}), 401

        if usuario.tipo_usuario() != 'superadmin':
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        return f(self, usuario, *args, **kwargs)
    return decorada

def usuario_opcional(f):
    @wraps(f)
    def decorada(self, *args, **kwargs):
        usuario = __extrair_usuario_do_token()
        return f(self, usuario, *args, **kwargs)
    return decorada