from flask import render_template, request, redirect, url_for, flash, session
from projeto.config import Config
from projeto.dao import UserDAO, HistoricoSenhaDAO
from projeto.models import User, HistoricoSenha
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sib_api_v3_sdk import ApiClient, TransactionalEmailsApi, SendSmtpEmail
import secrets

class HistoricoSenhaController:

    def __init__(self):
        self.__dao = UserDAO()
        self.__dao_historico = HistoricoSenhaDAO()

    def __verificar_senha(self, usuario, senha):
        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
            return False

        senhas_antigas = self.__dao_historico.listar_senhas_usuario(usuario.email)

        for hash_antigo in senhas_antigas:
            if check_password_hash(hash_antigo, senha):
                flash('Você não pode reutilizar uma das suas últimas senhas.', 'danger')
                return False

        if len(senhas_antigas) >= 5:
            self.__dao_historico.remover_senha_antiga(usuario.email)

        return True

    def __enviar_email_brevo(self, email_destino, link):

        html = render_template(
            "email_redefinir_senha.html",
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
        return render_template('recuperar_senha.html')

    def preparar_redefinir_senha(self, token):
        if 'usuario' in session:
            return render_template('erro.html')
        usuario = self.__dao.buscar_por_token(token)

        if not usuario:
            flash('Token inválido ou expirado.', 'danger')
            return redirect(url_for('user.login'))

        if usuario.token_expiracao and datetime.now() > usuario.token_expiracao:
            flash('Token expirado.', 'danger')
            return redirect(url_for('user.login'))

        return render_template('redefinir_senha.html', token=token)

    def enviar_recuperacao(self):
        email = request.form.get('email')

        usuario = self.__dao.buscar_usuario_por_email(email)

        flash('Se o email existir, enviaremos um link de recuperação.', 'success')

        if not usuario:
            return redirect(url_for('historico_senhas.recuperar_senha'))

        token = secrets.token_urlsafe(32)
        expiracao = datetime.now() + timedelta(hours=1)

        self.__dao.salvar_token_recuperacao(email, token, expiracao)

        link = f"http://localhost:5000/redefinir-senha/{token}"

        self.__enviar_email_brevo(email, link)

        return redirect(url_for('historico_senhas.recuperar_senha'))
    
    def redefinir_senha(self, token):
        senha = request.form.get('senha')
        confirmar = request.form.get('confirmar_senha')

        if senha != confirmar:
            flash('Senhas não coincidem.', 'danger')
            return redirect(request.url)

        usuario = self.__dao.buscar_por_token(token)

        if not usuario:
            flash('Token inválido.', 'danger')
            return redirect(url_for('user.login'))

        if not self.__verificar_senha(usuario, senha):
            return redirect(request.url)

        senha_hash = generate_password_hash(senha)

        usuario_atualizado = User(
                email=usuario.email,
                username=usuario.username,
                senha_hash=senha_hash,
                url_foto=usuario.url_foto,
                tipo_usuario=usuario.tipo_usuario
            )
        
        historico = HistoricoSenha(
            usuario=usuario,
            senha_hash=senha_hash
        )

        self.__dao.editar_usuario(usuario_atualizado)

        self.__dao_historico.inserir_nova_senha(historico)

        self.__dao.limpar_token(usuario.email)

        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('user.login'))