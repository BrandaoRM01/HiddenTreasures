from flask import flash, render_template, redirect, url_for, request, session
from projeto.dao import UserDAO
from projeto.models import User
from projeto.config import Config
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

class UserController:
    def __init__(self):
        self.__dao = UserDAO()

    def preparar_cadastro(self):
        return render_template('cadastro.html')
    
    def preparar_login(self):
        return render_template('login.html')
    
    def preparar_editar_perfil(self):
        return render_template('editar_perfil.html')
    
    def preparar_painel_admin(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        return render_template('painel_admin.html')
    
    def preparar_gerenciar_usuarios(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['superadmin', 'admin']:
            return render_template('erro.html')
        
        usuarios = self.__dao.listar_usuarios()
        return render_template('gerenciar_usuarios.html', usuarios=usuarios)
    
    def cadastrar_usuario(self):
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        username = request.form.get('username')
        foto = request.files.get('foto')
        
        usuario = self.__dao.buscar_usuario_por_email(email)

        lista_usernames = self.__dao.pegar_usernames()

        if usuario:
            flash('Email já cadastrado. Por favor, use outro email ou faça login.', 'danger')
            return redirect(url_for('user.cadastro'))

        if not email or not senha or not confirmar_senha or not username:
            flash('Informe os campos que são obrigatórios.', 'danger')
            return redirect(url_for('user.cadastro'))
        
        if username.capitalize().strip() in lista_usernames:
            flash('Nome de usuário já cadastrado. Por favor, escolha outro nome.', 'danger')
            return redirect(url_for('user.cadastro'))

        if senha != confirmar_senha:
            flash('As senhas não coincidem. Por favor, tente novamente.', 'danger')
            return redirect(url_for('user.cadastro'))

        senha_hash = generate_password_hash(senha)

        if not foto or foto.filename == "":
            nome_arquivo = "img/default/user_foto.webp"
        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(username.lower().replace(" ", "_"))
            
            nome_arquivo = f"uploads/user/{nome_ajustado}{extensao}"

            caminho = os.path.join(Config.UPLOAD_USER, f"{nome_ajustado}{extensao}")

            foto.save(caminho)

        novo_usuario = User(
            email=email,
            senha_hash=senha_hash,
            url_foto=nome_arquivo,
            username=username.capitalize().strip()
        )

        self.__dao.cadastrar_usuario(novo_usuario)

        flash('Cadastro realizado com sucesso! Faça login para acessar sua conta.', 'success')

        return redirect(url_for('user.login'))
    
    def autenticar_usuario(self):
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('user.login'))

        usuario = self.__dao.buscar_usuario_por_email(email)

        if not usuario:
            flash ('Usuário não encontrado. Por favor, verifique o email e tente novamente.', 'danger')
            return redirect(url_for('user.login'))

        if check_password_hash(usuario.senha_hash, senha):
            flash(f'Bem vindo, {usuario.username}!', 'success')
            session['usuario'] = usuario.to_dict()
            return redirect(url_for('pontos.index'))
        
        flash('Usuário ou senha incorretos. Por favor, tente novamente.', 'danger')
        return redirect(url_for('user.login'))
    
    def logout_usuario(self):
        if 'usuario' not in session:
            flash('Você precisa estar logado para sair de sua conta!', 'danger')
            return redirect(url_for('pontos.index'))
        
        session.pop('usuario', None)
        flash('Logout realizado com sucesso.', 'success')
        return redirect(url_for('pontos.index'))
    
    def excluir_usuario(self, email):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] != 'superadmin':
            return render_template('erro.html')

        self.__dao.excluir_usuario(email)
        flash('Usuário excluído com sucesso.', 'success')
        return redirect(url_for('user.gerenciar_usuarios'))
    
    def apagar_perfil(self, email):
        if 'usuario' not in session or session['usuario']['email'] != email:
            return render_template('erro.html')

        self.__dao.excluir_usuario(email)
        session.pop('usuario', None)
        flash('Perfil excluído com sucesso.', 'success')
        return redirect(url_for('pontos.index'))
    
    def alterar_permissao(self, usuario_email):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] != 'superadmin':
            return render_template('erro.html')
        
        if usuario_email == session['usuario']['email']:
            flash('Você não pode alterar sua própria permissão de usuário', 'danger')
            return redirect(url_for('user.gerenciar_usuarios'))

        usuario = self.__dao.buscar_usuario_por_email(usuario_email)  

        if not usuario:
            flash('Usuário não encontrado', 'danger')
            return redirect(url_for('user.gerenciar_usuarios'))

        if usuario.tipo_usuario == 'admin':
            usuario.tipo_usuario = 'user'
            self.__dao.alterar_permissao_usuario(usuario)
            
            flash('Permissão alterada com sucesso', 'success')
            return redirect(url_for('user.gerenciar_usuarios'))
        else:
            usuario.tipo_usuario = 'admin'
            self.__dao.alterar_permissao_usuario(usuario)
            
            flash('Permissão alterada com sucesso', 'success')
            return redirect(url_for('user.gerenciar_usuarios'))