from flask import render_template, request, jsonify
from projeto.dao import UserDAO, HistoricoSenhaDAO
from projeto.factorys import UsuarioFactory
from projeto.models import User, HistoricoSenha, usuario
from projeto.config import Config
from projeto.config import JWT
from projeto.decoradores import login_required, admin_required, superadmin_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import os

class UserController:
    def __init__(self):
        self.__dao_usuario = UserDAO()
        self.__dao_historico_senha = HistoricoSenhaDAO()

    def __verificar_senha(self, usuario, senha, senha_hash):
        if len(senha) < 8:
            return False, 'A senha deve ter pelo menos 8 caracteres.'

        senhas_antigas = self.__dao_historico_senha.listar_senhas_usuario(usuario.email)

        for hash_antigo in senhas_antigas:
            if check_password_hash(hash_antigo, senha):
                return False, 'Você não pode reutilizar uma das suas últimas cinco senhas.'

        if len(senhas_antigas) >= 5:
            self.__dao_historico_senha.remover_senha_antiga(usuario.email)

        return True, None

    def __validar_email(self, email):
        try:
            validate_email(email)
            return False
        except EmailNotValidError as e:
            print(f'Email inválido: {str(e)}')
            return True

    def preparar_cadastro(self):
        return render_template('usuario/cadastro.html')

    def preparar_login(self):
        return render_template('usuario/login.html')

    def preparar_editar_perfil(self):
        return render_template('usuario/editar_perfil.html')

    def preparar_painel_admin(self):
        return render_template('usuario/painel_admin.html')

    def preparar_gerenciar_usuarios(self):
        return render_template('usuario/gerenciar_usuarios.html')

    def preparar_favoritos(self):
        return render_template('ponto_turistico/favoritos.html')

    @login_required
    def listar_favoritos(self, usuario):
        favoritos = [ponto.to_dict() for ponto in usuario.pontos_favoritos]
        return jsonify(favoritos), 200

    @superadmin_required
    def listar_usuarios(self, usuario_logado):
        lista = self.__dao_usuario.listar_usuarios()
        usuarios = []

        for obj in lista:
            usuarios.append(obj.to_dict())

        dados = {
            'usuario_logado': usuario_logado.to_dict(),
            'usuarios': usuarios
        }

        return jsonify(dados), 200

    def cadastrar_usuario(self):
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        username = request.form.get('username')
        foto = request.files.get('foto')

        usuario = self.__dao_usuario.buscar_usuario_por_email(email)

        lista_usernames = self.__dao_usuario.pegar_usernames()

        if usuario:
            return jsonify({'mensagem': 'Email já cadastrado. Por favor, use outro email ou faça login.', 'classe': 'danger'}), 400

        if not email or not senha or not confirmar_senha or not username:
            return jsonify({'mensagem': 'Informe os campos que são obrigatórios.', 'classe': 'danger'}), 400

        if self.__validar_email(email):
            return jsonify({'mensagem': 'Email inválido. Por favor, informe um email válido.', 'classe': 'danger'}), 400

        if username.capitalize().strip() in lista_usernames:
            return jsonify({'mensagem': 'Nome de usuário já cadastrado. Por favor, escolha outro nome.', 'classe': 'danger'}), 400

        if senha != confirmar_senha:
            return jsonify({'mensagem': 'As senhas não coincidem. Por favor, tente novamente.', 'classe': 'danger'}), 400

        usuario_senha = UsuarioFactory.criar_usuario(
            email=email,
            username=username.capitalize().strip()
        )

        senha_hash = generate_password_hash(senha)

        if not self.__verificar_senha(usuario_senha, senha, senha_hash):
            return jsonify({'mensagem': 'Erro ao verificar a senha.', 'classe': 'danger'}), 400

        if not foto or foto.filename == "":
            nome_arquivo = "img/default/user_foto.webp"
        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(username.lower().replace(" ", "_"))

            nome_arquivo = f"uploads/user/{nome_ajustado}{extensao}"

            caminho = os.path.join(Config.UPLOAD_USER, f"{nome_ajustado}{extensao}")

            foto.save(caminho)

        novo_usuario = UsuarioFactory.criar_usuario(
            email=email,
            senha_hash=senha_hash,
            url_foto=nome_arquivo,
            username=username.capitalize().strip()
        )

        self.__dao_usuario.cadastrar_usuario(novo_usuario)

        historico = HistoricoSenha(novo_usuario, senha_hash)
        self.__dao_historico_senha.inserir_nova_senha(historico)

        return jsonify({'mensagem': 'Cadastro realizado com sucesso! Faça login para continuar.', 'classe': 'success'}), 200

    def autenticar_usuario(self):
        dados = request.get_json()
        email = dados.get('email')
        senha = dados.get('senha')

        if not email or not senha:
            return jsonify({'mensagem': 'Todos os campos são obrigatórios.', 'classe': 'danger'}), 400

        if self.__validar_email(email):
            return jsonify({'mensagem': 'Email inválido. Por favor, informe um email válido.', 'classe': 'danger'}), 400

        usuario = self.__dao_usuario.buscar_usuario_por_email(email)

        if not usuario:
            return jsonify({'mensagem': 'Usuário não encontrado. Por favor, verifique o email e tente novamente.', 'classe': 'danger'}), 400

        if check_password_hash(usuario.senha_hash, senha):
            token = JWT.gerar_token(usuario)
            return jsonify({'mensagem': f'Bem vindo, {usuario.username}!', 'classe': 'success', 'token': token}), 200

        return jsonify({'mensagem': 'Usuário ou senha incorretos. Por favor, tente novamente.', 'classe': 'danger'}), 400

    def logout_usuario(self):
        return jsonify({'mensagem': 'Logout realizado com sucesso.', 'classe': 'success'}), 200

    @login_required
    def me(self, usuario):
        return jsonify(usuario.to_dict()), 200

    @login_required
    def remover_usuario(self, usuario_logado, email):
        if email == 'me':
            email = usuario_logado.email
        proprio_perfil = (email == usuario_logado.email)

        if not proprio_perfil and not usuario_logado.pode_gerenciar_usuarios():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        usuario = self.__dao_usuario.buscar_usuario_por_email(email)

        if not usuario:
            return jsonify({'mensagem': 'Usuário não encontrado.', 'classe': 'danger'}), 400

        if not proprio_perfil and usuario.tipo_usuario() == 'superadmin':
            return jsonify({'mensagem': 'Não é possível excluir um superadmin.', 'classe': 'danger'}), 400

        self.__dao_usuario.excluir_usuario(email)

        if proprio_perfil:
            return jsonify({'mensagem': 'Perfil excluído com sucesso.', 'classe': 'success'}), 200

        return jsonify({'mensagem': 'Usuário excluído com sucesso.', 'classe': 'success'}), 200

    @login_required
    def editar_usuario(self, usuario_logado, email):
        if email == 'me':
            email = usuario_logado.email
        proprio_perfil = (email == usuario_logado.email)

        if not proprio_perfil and not usuario_logado.pode_gerenciar_usuarios():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        usuario = self.__dao_usuario.buscar_usuario_por_email(email)

        if not usuario:
            return jsonify({'mensagem': 'Usuário não encontrado.', 'classe': 'danger'}), 400

        tipo_usuario_recebido = request.form.get('tipo_usuario')

        if not proprio_perfil:
            if usuario.tipo_usuario() == 'superadmin':
                return jsonify({'mensagem': 'Não é possível alterar a permissão de um superadmin.', 'classe': 'danger'}), 400

            if tipo_usuario_recebido not in ['user', 'admin']:
                return jsonify({'mensagem': 'Tipo de usuário inválido.', 'classe': 'danger'}), 400

            self.__dao_usuario.alterar_permissao_usuario(usuario, tipo_usuario_recebido)

            return jsonify({'mensagem': 'Permissão alterada com sucesso!', 'classe': 'success'}), 200

        if tipo_usuario_recebido:
            return jsonify({'mensagem': 'Você não pode alterar sua própria permissão.', 'classe': 'danger'}), 400

        username = request.form.get('username')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        foto = request.files.get('foto')

        lista_usernames = self.__dao_usuario.pegar_usernames()

        if not username:
            return jsonify({'mensagem': 'Informe o campo obrigatório.', 'classe': 'danger'}), 400

        username_ajustado = username.capitalize().strip()

        if username_ajustado in lista_usernames and username_ajustado != usuario.username:
            return jsonify({'mensagem': 'Username já está em uso por outro usuário. Tente outro nome.', 'classe': 'danger'}), 400

        senha_hash = usuario.senha_hash
        senha_alterada = False

        if senha and confirmar_senha:
            if senha != confirmar_senha:
                return jsonify({'mensagem': 'As senhas não coincidem.', 'classe': 'danger'}), 400

            senha_hash_nova = generate_password_hash(senha)

            senha_valida, mensagem_erro = self.__verificar_senha(usuario, senha, senha_hash_nova)

            if not senha_valida:
                return jsonify({'mensagem': mensagem_erro, 'classe': 'danger'}), 400

            senha_hash = senha_hash_nova
            senha_alterada = True

        if senha and not confirmar_senha:
            return jsonify({'mensagem': 'Se você quer mudar sua senha, informe também a confirmação de senha.', 'classe': 'danger'}), 400

        username_antigo = usuario.username
        nome_antigo = os.path.basename(usuario.url_foto)

        if not foto or foto.filename == "":
            if username_antigo != username_ajustado and "default" not in usuario.url_foto:
                extensao = os.path.splitext(nome_antigo)[1]
                nome_ajustado_file = secure_filename(username_ajustado.lower().replace(" ", "_"))
                novo_nome = f"{nome_ajustado_file}{extensao}"

                caminho_antigo = os.path.join(Config.UPLOAD_USER, nome_antigo)
                caminho_novo = os.path.join(Config.UPLOAD_USER, novo_nome)

                if os.path.exists(caminho_antigo):
                    if os.path.exists(caminho_novo):
                        os.remove(caminho_novo)
                    os.rename(caminho_antigo, caminho_novo)

                nome_arquivo = f"uploads/user/{novo_nome}"
            else:
                nome_arquivo = usuario.url_foto
        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado_file = secure_filename(username_ajustado.lower().replace(" ", "_"))
            novo_nome = f"{nome_ajustado_file}{extensao}"
            caminho = os.path.join(Config.UPLOAD_USER, novo_nome)

            if "default" not in usuario.url_foto:
                caminho_antigo = os.path.join(Config.UPLOAD_USER, nome_antigo)
                if os.path.exists(caminho_antigo):
                    os.remove(caminho_antigo)

            foto.stream.seek(0)
            foto.save(caminho)

            nome_arquivo = f"uploads/user/{novo_nome}"

        usuario_atualizado = UsuarioFactory.criar_usuario(
            email=usuario.email,
            senha_hash=senha_hash,
            url_foto=nome_arquivo,
            username=username_ajustado,
            tipo_usuario=usuario.tipo_usuario()
        )

        self.__dao_usuario.editar_usuario(usuario_atualizado)

        if senha_alterada:
            historico = HistoricoSenha(usuario_atualizado, senha_hash)
            self.__dao_historico_senha.inserir_nova_senha(historico)

        return jsonify({'mensagem': 'Usuário atualizado com sucesso!', 'classe': 'success'}), 200

    @login_required
    def alterar_favorito(self, usuario):
        dados = request.get_json()
        ponto_id = dados.get('ponto_id')

        if not ponto_id:
            return jsonify({'mensagem': 'Ponto turístico não encontrado', 'classe': 'danger'}), 400

        if self.__dao_usuario.verificar_favorito(usuario.email, ponto_id):
            self.__dao_usuario.deletar_favorito(usuario.email, ponto_id)
            favorito = False
            mensagem = 'Ponto turístico desfavoritado com sucesso'
        else:
            self.__dao_usuario.adicionar_favorito(ponto_id, usuario.email)
            favorito = True
            mensagem = 'Ponto turístico favoritado com sucesso!'

        return jsonify({'mensagem': mensagem, 'classe': 'success', 'favorito': favorito}), 200

    @login_required
    def buscar_usuario_por_email(self, usuario_logado, email):
        if email == 'me':
            email = usuario_logado.email
        usuario = self.__dao_usuario.buscar_usuario_por_email(email)

        if not usuario:
            return jsonify({'mensagem': 'Usuário não encontrado.', 'classe': 'danger'}), 400

        return jsonify(usuario.to_dict()), 200