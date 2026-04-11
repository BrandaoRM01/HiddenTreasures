from flask import flash, render_template, redirect, url_for, request, session
from projeto.dao import UserDAO, HistoricoSenhaDAO
from projeto.models import User, HistoricoSenha
from projeto.config import Config
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

class UserController:
    def __init__(self):
        self.__dao_usuario = UserDAO()
        self.__dao_historico_senha = HistoricoSenhaDAO()

    def __verificar_senha(self, usuario, senha, senha_hash):
        if len(senha) < 8:
            flash('A senha deve ter pelo menos 8 caracteres.', 'danger')
            return False

        senhas_antigas = self.__dao_historico_senha.listar_senhas_usuario(usuario.email)

        for hash_antigo in senhas_antigas:
            if check_password_hash(hash_antigo, senha):
                flash('Você não pode reutilizar uma das suas últimas cinco senhas.', 'danger')
                return False

        if len(senhas_antigas) >= 5:
            self.__dao_historico_senha.remover_senha_antiga(usuario.email)

        return True

    def preparar_cadastro(self):
        if 'usuario' in session:
            return render_template('erro.html')
        return render_template('cadastro.html')
    
    def preparar_login(self):
        if 'usuario' in session:
            return render_template('erro.html')
        return render_template('login.html')
    
    def preparar_editar_perfil(self):
        if 'usuario' not in session:
            return render_template('erro.html')
        
        return render_template('editar_perfil.html')
    
    def preparar_painel_admin(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:

            return render_template('erro.html')
        return render_template('painel_admin.html')
    
    def preparar_gerenciar_usuarios(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['superadmin', 'admin']:
            return render_template('erro.html')
        
        usuarios = self.__dao_usuario.listar_usuarios()
        return render_template('gerenciar_usuarios.html', usuarios=usuarios)
    
    def cadastrar_usuario(self):
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        username = request.form.get('username')
        foto = request.files.get('foto')
        
        usuario = self.__dao_usuario.buscar_usuario_por_email(email)

        lista_usernames = self.__dao_usuario.pegar_usernames()

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
        
        usuario_senha = User(
            email=email,
            username=username.capitalize().strip()
        )

        senha_hash = generate_password_hash(senha)

        if not self.__verificar_senha(usuario_senha, senha, senha_hash):
            return redirect(url_for('user.cadastro'))

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

        self.__dao_usuario.cadastrar_usuario(novo_usuario)

        historico = HistoricoSenha(novo_usuario, senha_hash)
        self.__dao_historico_senha.inserir_nova_senha(historico)

        flash('Cadastro realizado com sucesso! Faça login para acessar sua conta.', 'success')

        return redirect(url_for('user.login'))
    
    def autenticar_usuario(self):
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('user.login'))

        usuario = self.__dao_usuario.buscar_usuario_por_email(email)

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

        self.__dao_usuario.excluir_usuario(email)
        flash('Usuário excluído com sucesso.', 'success')
        return redirect(url_for('user.gerenciar_usuarios'))
    
    def apagar_perfil(self, email):
        if 'usuario' not in session or session['usuario']['email'] != email or session['usuario']['tipo_usuario'] == 'superadmin':
            return render_template('erro.html')

        self.__dao_usuario.excluir_usuario(email)
        session.pop('usuario', None)
        flash('Perfil excluído com sucesso.', 'success')
        return redirect(url_for('pontos.index'))
    
    def alterar_permissao(self, usuario_email):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] != 'superadmin':
            return render_template('erro.html')
        
        if usuario_email == session['usuario']['email']:
            flash('Você não pode alterar sua própria permissão de usuário', 'danger')
            return redirect(url_for('user.gerenciar_usuarios'))

        usuario = self.__dao_usuario.buscar_usuario_por_email(usuario_email)  

        if not usuario:
            flash('Usuário não encontrado', 'danger')
            return redirect(url_for('user.gerenciar_usuarios'))

        if usuario.tipo_usuario == 'admin':
            usuario.tipo_usuario = 'user'
            self.__dao_usuario.alterar_permissao_usuario(usuario)
            
            flash('Permissão alterada com sucesso', 'success')
            return redirect(url_for('user.gerenciar_usuarios'))
        else:
            usuario.tipo_usuario = 'admin'
            self.__dao_usuario.alterar_permissao_usuario(usuario)
            
            flash('Permissão alterada com sucesso', 'success')
            return redirect(url_for('user.gerenciar_usuarios'))
        
    def editar_perfil(self):
        if 'usuario' not in session:
            return render_template('erro.html')
        
        email = session['usuario']['email']
        username = request.form.get('username')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')
        foto = request.files.get('foto')

        usuario = self.__dao_usuario.buscar_usuario_por_email(email)
        lista_usernames = self.__dao_usuario.pegar_usernames()

        if not username:
            flash('Informe o campo obrigatório.', 'danger')
            return redirect(url_for('user.editar_perfil'))
        
        if not usuario:
            flash('Usuário não encontrado no sistema.', 'danger')
            return redirect(url_for('pontos.index'))

        username_ajustado = username.capitalize().strip()

        if username_ajustado in lista_usernames and username_ajustado != session['usuario']['username']:
            flash('Username já está em uso por outro usuário. Tente outro nome.', 'danger')
            return redirect(url_for('user.editar_perfil'))
        
        senha_hash = usuario.senha_hash
        senha_alterada = False

        if senha and confirmar_senha:
            if senha != confirmar_senha:
                flash('As senhas não coincidem.', 'danger')
                return redirect(url_for('user.editar_perfil'))

            senha_hash_nova = generate_password_hash(senha)

            if not self.__verificar_senha(usuario, senha, senha_hash_nova):
                return redirect(url_for('user.editar_perfil'))
            
            senha_hash = senha_hash_nova
            senha_alterada = True

        if senha and not confirmar_senha:
            flash('Se você quer mudar sua senha, informe também a confirmação de senha.', 'danger')
            return redirect(url_for('user.editar_perfil'))

        username_antigo = usuario.username
        nome_antigo = os.path.basename(usuario.url_foto)

        if not foto or foto.filename == "":
            
            if username_antigo != username_ajustado:

                if "default" not in usuario.url_foto:
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

        tipo_usuario = session['usuario']['tipo_usuario']

        usuario_atualizado = User(
            email=email,
            senha_hash=senha_hash,
            url_foto=nome_arquivo,
            username=username_ajustado,
            tipo_usuario=tipo_usuario
        )

        self.__dao_usuario.editar_usuario(usuario_atualizado)

        if senha_alterada:
            historico = HistoricoSenha(usuario_atualizado, senha_hash)
            self.__dao_historico_senha.inserir_nova_senha(historico)

        session['usuario'] = usuario_atualizado.to_dict()

        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('pontos.index'))