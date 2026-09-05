from flask import render_template, request, session, jsonify
from projeto.config import Config
from projeto.dao import UserDAO, HistoricoSenhaDAO
from projeto.factorys import UsuarioFactory, HistoricoSenhaFactory
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sib_api_v3_sdk import ApiClient, TransactionalEmailsApi, SendSmtpEmail
from email_validator import validate_email, EmailNotValidError
import secrets

class HistoricoSenhaController:

    def __init__(self):
        self.__dao = UserDAO()
        self.__dao_historico = HistoricoSenhaDAO()

    def __verificar_senha(self, usuario, senha):
        if len(senha) < 8:
            return False, 'A senha deve ter pelo menos 8 caracteres.'

        senhas_antigas = self.__dao_historico.listar_senhas_usuario(usuario.email)

        for hash_antigo in senhas_antigas:
            if check_password_hash(hash_antigo, senha):
                return False, 'Você não pode reutilizar uma das suas últimas senhas.'

        if len(senhas_antigas) >= 5:
            self.__dao_historico.remover_senha_antiga(usuario.email)

        return True, None

    def __validar_email(self, email):
        try:
            validate_email(email)
            return False
        except EmailNotValidError as e:
            print(f'Email inválido: {str(e)}')
            return True

    def __enviar_email_brevo(self, email_destino, link):
        html = render_template(
            "usuario/email_redefinir_senha.html",
            link=link
        )

        api_client = ApiClient(Config.BREVO_CONFIG)
        api_instance = TransactionalEmailsApi(api_client)

        email = SendSmtpEmail(
            sender={
                "name": "HiddenTreasures",
                "email": "raulmb231@gmail.com"
            },
            to=[{"email": email_destino}],
            subject="Recuperação de Senha - HiddenTreasures",
            html_content=html
        )

        try:
            api_instance.send_transac_email(email)
            return True
        except Exception as e:
            print("Erro ao enviar email:", e)
            return False

    def preparar_recuperar_senha(self):
        if 'usuario' in session:
            return render_template('erro.html')
        return render_template('usuario/recuperar_senha.html')

    def preparar_redefinir_senha(self, token):
        if 'usuario' in session:
            return render_template('erro.html')

        usuario = self.__dao.buscar_por_token(token)

        if not usuario:
            return render_template('erro.html')

        if usuario.token_expiracao and datetime.now() > usuario.token_expiracao:
            return render_template('erro.html')

        return render_template('usuario/redefinir_senha.html', token=token)

    def enviar_recuperacao(self):
        dados = request.get_json()
        email = dados.get('email')

        if not email:
            return jsonify({'mensagem': 'Informe o campo obrigatório.', 'classe': 'danger'}), 400

        if self.__validar_email(email):
            return jsonify({'mensagem': 'Email inválido. Por favor, informe um email válido.', 'classe': 'danger'}), 400

        usuario = self.__dao.buscar_usuario_por_email(email)

        if not usuario:
            return jsonify({'mensagem': 'Se o email existir, enviaremos um link de recuperação.', 'classe': 'success'}), 200

        token = secrets.token_urlsafe(32)
        expiracao = datetime.now() + timedelta(hours=1)

        self.__dao.salvar_token_recuperacao(email, token, expiracao)

        link = f"http://localhost:5000/redefinir-senha/{token}"

        self.__enviar_email_brevo(email, link)

        return jsonify({'mensagem': 'Se o email existir, enviaremos um link de recuperação.', 'classe': 'success'}), 200

    def redefinir_senha(self, token):
        dados = request.get_json()
        senha = dados.get('senha')
        confirmar = dados.get('confirmar_senha')

        if not senha or not confirmar:
            return jsonify({'mensagem': 'Informe os campos obrigatórios.', 'classe': 'danger'}), 400

        if senha != confirmar:
            return jsonify({'mensagem': 'Senhas não coincidem.', 'classe': 'danger'}), 400

        usuario = self.__dao.buscar_por_token(token)

        if not usuario:
            return jsonify({'mensagem': 'Token inválido.', 'classe': 'danger'}), 400

        if usuario.token_expiracao and datetime.now() > usuario.token_expiracao:
            return jsonify({'mensagem': 'Token expirado.', 'classe': 'danger'}), 400

        senha_valida, mensagem_erro = self.__verificar_senha(usuario, senha)

        if not senha_valida:
            return jsonify({'mensagem': mensagem_erro, 'classe': 'danger'}), 400

        senha_hash = generate_password_hash(senha)

        usuario_atualizado = UsuarioFactory.criar_usuario(
            email=usuario.email,
            username=usuario.username,
            senha_hash=senha_hash,
            url_foto=usuario.url_foto,
            tipo_usuario=usuario.tipo_usuario()
        )

        historico = HistoricoSenhaFactory.criar_historico_senha(
            usuario=usuario,
            senha_hash=senha_hash
        )

        self.__dao.editar_usuario(usuario_atualizado)
        self.__dao_historico.inserir_nova_senha(historico)
        self.__dao.limpar_token(usuario.email)

        return jsonify({'mensagem': 'Senha alterada com sucesso!', 'classe': 'success'}), 200