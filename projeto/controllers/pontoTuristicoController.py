from flask import flash, render_template, redirect, url_for, request, session
from projeto.dao import PontoTuristicoDAO, CategoriaDAO, AvaliacaoDAO, PromocaoDAO
from projeto.models import PontoTuristico, Categoria, Promocao
from projeto.config import Config
from werkzeug.utils import secure_filename
import os

class PontoTuristicoController:

    def __init__(self):
        self.__dao_pontos = PontoTuristicoDAO()
        self.__dao_categorias = CategoriaDAO()
        self.__dao_avaliacoes = AvaliacaoDAO()
        self.__dao_promocoes = PromocaoDAO()

    def __listar_pontos(self):
        return self.__dao_pontos.listar_pontos()
    
    def preparar_index(self):
        pontos_promocao = []

        top_pontos = self.__dao_pontos.listar_top_pontos()
        pontos = self.__dao_pontos.listar_pontos()

        if not pontos:
            pontos = None

        if not top_pontos:
            top_pontos = None

        for ponto in pontos:
            if ponto.promocao != None:
                pontos_promocao.append(ponto)

        return render_template('index.html', pontos_promocao=pontos_promocao, top_pontos=top_pontos)
    
    def preparar_sobre(self):
        return render_template('sobre.html')

    def preparar_gerenciar_pontos(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        lista_pontos = self.__listar_pontos()
        lista_categorias = self.__dao_categorias.carregar_categorias()
        lista_promocoes = self.__dao_promocoes.listar_promocoes_ativas()

        return render_template('gerenciar_pontos.html', lista_pontos=lista_pontos, lista_categorias=lista_categorias, lista_promocoes=lista_promocoes)
    
    def preparar_editar_ponto(self, id_ponto):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.gerenciar_pontos'))

        lista_categorias = self.__dao_categorias.carregar_categorias()
        lista_promocoes = self.__dao_promocoes.listar_promocoes_ativas()

        return render_template('editar_ponto.html', ponto=ponto, lista_categorias=lista_categorias, lista_promocoes=lista_promocoes)
    
    def preparar_pontos_turisticos(self):
        lista_pontos = self.__listar_pontos()
        return render_template('pontos.html', lista_pontos=lista_pontos)
    
    def preparar_detalhes_ponto(self, id_ponto):
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)
        usuario_email = None

        if not ponto:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.pontos_turisticos'))
        
        if 'usuario' in session:
            usuario_email = session['usuario']['email']

        avaliacoes = self.__dao_avaliacoes.listar_ultimas_avaliacoes_ponto(id_ponto, usuario_email)

        avaliacao_usuario = self.__dao_avaliacoes.buscar_avaliacao(usuario_email, id_ponto)

        avaliacoes_ponto = self.__dao_avaliacoes.listar_avaliacoes_por_ponto(id_ponto, usuario_email)

        if not avaliacao_usuario:
            avaliacao_usuario = None

        return render_template('detalhes_ponto.html', ponto=ponto, avaliacoes=avaliacoes, avaliacao_usuario=avaliacao_usuario, quantidade=len(avaliacoes_ponto) )
    
    def cadastrar_ponto(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        descricao = request.form.get('descricao')
        horario_funcionamento = request.form.get('horario_funcionamento')
        custo_entrada = request.form.get('custo_entrada')
        categoria_id = request.form.get('categoria')
        promocao_id = request.form.get('promocao')
        foto = request.files.get('foto')

        if not nome or not localizacao or not descricao or not categoria_id:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('pontos.gerenciar_pontos'))
        
        if not custo_entrada:
            custo_entrada = 0.0
        else:
            try:
                custo_entrada = float(custo_entrada)
            except (ValueError, TypeError):
                flash('Por favor, insira um valor válido para o custo de entrada.', 'danger')
                return redirect(url_for('pontos.gerenciar_pontos'))
            
        if not horario_funcionamento:
            horario_funcionamento = "Não informado"

        if not foto or foto.filename == "":
            nome_arquivo = "img/default/hidden_treasures_logo.png"
        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(nome.lower().replace(" ", "_"))
            
            nome_arquivo = f"uploads/pontos/{nome_ajustado}{extensao}"

            caminho = os.path.join(Config.UPLOAD_PONTOS, f"{nome_ajustado}{extensao}")

            foto.save(caminho)

        categoria_dados = self.__dao_categorias.buscar_categoria_por_id(categoria_id)

        if not categoria_dados:
            flash('Categoria selecionada não encontrada.', 'danger')
            return redirect(url_for('pontos.gerenciar_pontos'))
        
        categoria = Categoria(
            id=categoria_dados['id'],
            nome=categoria_dados['nome'],
            descricao=categoria_dados['descricao']
        )

        promocao_dados = self.__dao_promocoes.pegar_promocao_por_id(promocao_id)

        if custo_entrada <= 10 and promocao_dados:
            flash('Você não pode definir uma promocão para um ponto abaixo de R$10.', 'danger')
            return redirect(url_for('pontos.gerenciar_pontos'))

        if promocao_dados:
            promocao = Promocao(
                id=promocao_dados['id'],
                titulo=promocao_dados['titulo'],
                data_inicio=promocao_dados['data_inicio'],
                data_fim=promocao_dados['data_fim'],
                desconto=promocao_dados['desconto']
            )
        else:
            promocao = None

        novo_ponto = PontoTuristico(
            nome=nome.capitalize().strip(),
            localizacao=localizacao.capitalize().strip(),
            descricao=descricao.capitalize().strip(),
            horario_funcionamento=horario_funcionamento.capitalize().strip(),
            custo_entrada=custo_entrada,
            categoria=categoria,
            promocao=promocao,
            url_imagem=nome_arquivo
        )

        self.__dao_pontos.cadastrar_ponto(novo_ponto)

        return self.preparar_gerenciar_pontos()
    
    def remover_ponto(self, id_ponto):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
                return render_template('erro.html')
        
        self.__dao_pontos.excluir_ponto(id_ponto)
        return self.preparar_gerenciar_pontos()
    
    def editar_ponto(self, id_ponto):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        descricao = request.form.get('descricao')
        horario_funcionamento = request.form.get('horario_funcionamento')
        custo_entrada = request.form.get('custo_entrada')
        categoria_id = request.form.get('categoria')
        promocao_id = request.form.get('promocao')
        foto = request.files.get('foto')

        if not nome or not localizacao or not descricao or not categoria_id:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('pontos.editar_ponto', id=id_ponto))
        
        if not custo_entrada:
            custo_entrada = 0.0
        else:
            try:
                custo_entrada = float(custo_entrada)
            except (ValueError, TypeError):
                flash('Por favor, insira um valor válido para o custo de entrada.', 'danger')
                return redirect(url_for('pontos.editar_ponto', id=id_ponto))
            
        if not horario_funcionamento:
            horario_funcionamento = "Não informado"

        ponto_existente = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto_existente:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.gerenciar_pontos'))

        if not foto or foto.filename == "":
            nome_arquivo = ponto_existente.url_imagem
        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_ajustado = secure_filename(nome.lower().replace(" ", "_"))
            
            nome_arquivo = f"uploads/pontos/{nome_ajustado}{extensao}"

            caminho = os.path.join(Config.UPLOAD_PONTOS, f"{nome_ajustado}{extensao}")

            foto.save(caminho)

        categoria_dados = self.__dao_categorias.buscar_categoria_por_id(categoria_id)

        if not categoria_dados:
            flash('Categoria selecionada não encontrada.', 'danger')
            return redirect(url_for('pontos.editar_ponto', id=id_ponto))

        categoria = Categoria(
            id=categoria_dados['id'],
            nome=categoria_dados['nome'],
            descricao=categoria_dados['descricao']
        )

        promocao_dados = self.__dao_promocoes.pegar_promocao_por_id(promocao_id)

        if custo_entrada <= 10 and promocao_dados:
            flash('Você não pode definir uma promocão para um ponto abaixo de R$10.', 'danger')
            return redirect(url_for('pontos.editar_ponto', id=id_ponto))

        if promocao_dados:

            promocao = Promocao(
                id=promocao_dados['id'],
                titulo=promocao_dados['titulo'],
                data_inicio=promocao_dados['data_inicio'],
                data_fim=promocao_dados['data_fim'],
                desconto=promocao_dados['desconto']
            )
        else:
            promocao = None

        ponto_atualizado = PontoTuristico(
            id=id_ponto,
            nome=nome.capitalize().strip(),
            localizacao=localizacao.capitalize().strip(),
            descricao=descricao.capitalize().strip(),
            horario_funcionamento=horario_funcionamento.capitalize().strip(),
            custo_entrada=custo_entrada,
            categoria=categoria,
            promocao=promocao,
            url_imagem=nome_arquivo
        )

        imagem_antiga = ponto_existente.url_imagem

        self.__dao_pontos.atualizar_ponto(ponto_atualizado, imagem_antiga)

        return self.preparar_gerenciar_pontos()
    
    def listar_pontos_busca(self):
        escrita = request.form.get('escrita')
        filtro = request.form.get('filtro')

        if not escrita or not filtro:
            flash('Para pesquisar um ponto turístico é necessário informar o filtro e a escrita', 'danger')

        if escrita:
            escrita = escrita.capitalize().strip()

        lista_pontos = self.__dao_pontos.buscar_pontos(escrita, filtro)

        return render_template('pontos_busca.html', lista_pontos=lista_pontos)