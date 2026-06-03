from flask import flash, render_template, redirect, url_for, request, session
from projeto.dao import PontoTuristicoDAO, CategoriaDAO, UserDAO, PromocaoDAO, TipoCulturalDAO, EcossistemaDAO
from projeto.factorys import PontoTuristicoFactory, CategoriaFactory, PromocaoFactory, TipoCulturalFactory, EcossistemaFactory
from projeto.config import Config
from werkzeug.utils import secure_filename
import os

class PontoTuristicoController:

    def __init__(self):
        self.__dao_pontos = PontoTuristicoDAO()
        self.__dao_categorias = CategoriaDAO()
        self.__dao_usuario = UserDAO()
        self.__dao_promocoes = PromocaoDAO()
        self.__dao_tipo_cultural = TipoCulturalDAO()
        self.__dao_ecossistema = EcossistemaDAO()

    def __listar_pontos(self):
        return self.__dao_pontos.listar_pontos()
    
    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def preparar_index(self):
        pontos_promocao = []

        top_pontos = self.__dao_pontos.listar_top_pontos()
        pontos = self.__dao_pontos.listar_pontos()

        if not pontos:
            pontos = None

        if not top_pontos:
            top_pontos = None

        if pontos:
            for ponto in pontos:
                if ponto.promocao != None:
                    pontos_promocao.append(ponto)
        
        if session.get('usuario'):
            usuario_email = session['usuario']['email']
            usuario = self.__dao_usuario.buscar_usuario_por_email(usuario_email)

            favoritos_ids = [ponto.id for ponto in usuario.pontos_favoritos]
        else:
            favoritos_ids = []
   
        return render_template('index.html', pontos_promocao=pontos_promocao, top_pontos=top_pontos, favoritos_ids=favoritos_ids)

    def preparar_sobre(self):
        return render_template('sobre.html')

    def preparar_gerenciar_pontos(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        lista_pontos = self.__listar_pontos()
        lista_categorias = self.__dao_categorias.carregar_categorias()
        lista_promocoes = self.__dao_promocoes.listar_promocoes_ativas()

        return render_template('gerenciar_pontos.html', lista_pontos=lista_pontos, lista_categorias=lista_categorias, lista_promocoes=lista_promocoes)
    
    def preparar_editar_ponto(self, id_ponto):
        if not self.__usuario_pode_moderar():
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

        if session.get('usuario'):
            usuario_email = session['usuario']['email']
            usuario = self.__dao_usuario.buscar_usuario_por_email(usuario_email)

            favoritos_ids = [ponto.id for ponto in usuario.pontos_favoritos]
        else:
            favoritos_ids = []

        return render_template('pontos.html', lista_pontos=lista_pontos, favoritos_ids=favoritos_ids)

    def preparar_detalhes_ponto(self, id_ponto):
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)
        usuario_email = None
        avaliacao_usuario = None

        if not ponto:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.pontos'))
        
        if 'usuario' in session:
            usuario_email = session['usuario']['email']

        for avaliacao in ponto.avaliacoes:
            if usuario_email and avaliacao.usuario.email == usuario_email:
                avaliacao_usuario = avaliacao
                break

        ultimas_avaliacoes = ponto.avaliacoes[-5:]

        return render_template('detalhes_ponto.html', ponto=ponto, avaliacoes=ultimas_avaliacoes, avaliacao_usuario=avaliacao_usuario, quantidade=len(ponto.avaliacoes))
    
    def cadastrar_ponto(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        descricao = request.form.get('descricao')
        horario_funcionamento = request.form.get('horario_funcionamento')
        custo_entrada = request.form.get('custo_entrada')
        categoria_id = request.form.get('categoria')
        promocao_id = request.form.get('promocao')
        foto = request.files.get('foto')
        tipo_ponto = request.form.get('tipo_ponto')
        tipo_cultural_id = request.form.get('tipo_cultural')
        ano_fundacao = request.form.get('ano_fundacao')
        ecossistema_id = request.form.get('ecossistema')
        area_km = request.form.get('area_km')

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
            
        if tipo_ponto == 'natural':
            try:
                area_km = float(area_km)
            except (ValueError, TypeError):
                flash('Por favor, insira um valor válido para a área.', 'danger')
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
        
        categoria = CategoriaFactory.criar_categoria(
            id=categoria_dados['id'],
            nome=categoria_dados['nome'],
            descricao=categoria_dados['descricao']
        )

        promocao_dados = self.__dao_promocoes.pegar_promocao_por_id(promocao_id)

        if custo_entrada <= 10 and promocao_dados:
            flash('Você não pode definir uma promocão para um ponto abaixo de R$10.', 'danger')
            return redirect(url_for('pontos.gerenciar_pontos'))

        if promocao_dados:
            promocao = PromocaoFactory.criar_promocao(
                id=promocao_dados.id,
                titulo=promocao_dados.titulo,
                data_inicio=promocao_dados.data_inicio,
                data_fim=promocao_dados.data_fim,
                desconto=promocao_dados.desconto
            )
        else:
            promocao = None

        if tipo_ponto == "cultural":
            tipo_cultural_dados = self.__dao_tipo_cultural.buscar_tipo_por_id(tipo_cultural_id)

            if not tipo_cultural_dados:
                flash('Tipo cultural selecionado não encontrado.', 'danger')
                return redirect(url_for('pontos.gerenciar_pontos'))

            tipo_cultural = TipoCulturalFactory.criar_tipo_cultural(
                id=tipo_cultural_dados.id,
                nome=tipo_cultural_dados.nome
            )

            novo_ponto = PontoTuristicoFactory.criar_ponto_turistico(
                nome=nome.capitalize().strip(),
                localizacao=localizacao.capitalize().strip(),
                descricao=descricao.capitalize().strip(),
                horario_funcionamento=horario_funcionamento.capitalize().strip(),
                custo_entrada=custo_entrada,
                categoria=categoria,
                promocao=promocao,
                url_imagem=nome_arquivo,
                tipo_cultural=tipo_cultural,
                ano_fundacao=ano_fundacao.strip() if ano_fundacao else "Não informado",
                status="aprovado",
                tipo_ponto=tipo_ponto
            )
        else:
            ecossistema_dados = self.__dao_ecossistema.buscar_ecossistema_por_id(ecossistema_id)

            if not ecossistema_dados:
                flash('Ecossistema selecionado não encontrado.', 'danger')
                return redirect(url_for('pontos.gerenciar_pontos'))

            ecossistema = EcossistemaFactory.criar_ecossistema(
                id=ecossistema_dados.id,
                nome=ecossistema_dados.nome
            )

            novo_ponto = PontoTuristicoFactory.criar_ponto_turistico(
                nome=nome.capitalize().strip(),
                localizacao=localizacao.capitalize().strip(),
                descricao=descricao.capitalize().strip(),
                horario_funcionamento=horario_funcionamento.capitalize().strip(),
                custo_entrada=custo_entrada,
                categoria=categoria,
                promocao=promocao,
                url_imagem=nome_arquivo,
                tipo_ponto=tipo_ponto,
                ecossistema=ecossistema,
                area_km=area_km if area_km else 0,
                status="aprovado"
            )


        self.__dao_pontos.cadastrar_ponto(novo_ponto)

        flash('Ponto turístico cadastrado com sucesso!', 'success')
        return self.preparar_gerenciar_pontos()
    
    def remover_ponto(self, id_ponto):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        self.__dao_pontos.excluir_ponto(id_ponto)
        flash('Ponto turístico excluído com sucesso!', 'success')
        return self.preparar_gerenciar_pontos()
    
    def editar_ponto(self, id_ponto):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        nome = request.form.get('nome')
        localizacao = request.form.get('localizacao')
        descricao = request.form.get('descricao')
        horario_funcionamento = request.form.get('horario_funcionamento')
        custo_entrada = request.form.get('custo_entrada')
        categoria_id = request.form.get('categoria')
        promocao_id = request.form.get('promocao')
        foto = request.files.get('foto')
        tipo_ponto = request.form.get('tipo_ponto')
        tipo_cultural_id = request.form.get('tipo_cultural')
        ano_fundacao = request.form.get('ano_fundacao')
        ecossistema_id = request.form.get('ecossistema')
        area_km = request.form.get('area_km')

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
            
        if tipo_ponto == 'natural':
            try:
                area_km = float(area_km)
            except (ValueError, TypeError):
                flash('Por favor, insira um valor válido para a área.', 'danger')
                return redirect(url_for('pontos.editar_ponto', id=id_ponto))
            
        if not horario_funcionamento:
            horario_funcionamento = "Não informado"

        ponto_existente = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto_existente:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.gerenciar_pontos'))

        nome_antigo = os.path.basename(ponto_existente.url_imagem)
        nome_antigo_ponto = ponto_existente.nome

        nome_ajustado = nome.capitalize().strip()

        if not foto or foto.filename == "":
            
            if nome_antigo_ponto != nome_ajustado:

                if ponto_existente.url_imagem and "default" not in ponto_existente.url_imagem:
                    extensao = os.path.splitext(nome_antigo)[1]
                    nome_base = secure_filename(nome_ajustado.lower().replace(" ", "_"))

                    novo_nome = f"{nome_base}{extensao}"

                    caminho_antigo = os.path.join(Config.UPLOAD_PONTOS, nome_antigo)
                    caminho_novo = os.path.join(Config.UPLOAD_PONTOS, novo_nome)

                    if os.path.exists(caminho_antigo):
                        if os.path.exists(caminho_novo):
                            os.remove(caminho_novo)

                        os.rename(caminho_antigo, caminho_novo)

                    nome_arquivo = f"uploads/pontos/{novo_nome}"
                else:
                    nome_arquivo = ponto_existente.url_imagem
            else:
                nome_arquivo = ponto_existente.url_imagem

        else:
            extensao = os.path.splitext(foto.filename)[1]
            nome_base = secure_filename(nome_ajustado.lower().replace(" ", "_"))

            novo_nome = f"{nome_base}{extensao}"
            caminho = os.path.join(Config.UPLOAD_PONTOS, novo_nome)

            if ponto_existente.url_imagem and "default" not in ponto_existente.url_imagem:
                caminho_antigo = os.path.join(Config.UPLOAD_PONTOS, nome_antigo)
                if os.path.exists(caminho_antigo):
                    os.remove(caminho_antigo)

            foto.stream.seek(0)
            foto.save(caminho)

            nome_arquivo = f"uploads/pontos/{novo_nome}"

        categoria_dados = self.__dao_categorias.buscar_categoria_por_id(categoria_id)

        if not categoria_dados:
            flash('Categoria selecionada não encontrada.', 'danger')
            return redirect(url_for('pontos.editar_ponto', id=id_ponto))

        categoria = CategoriaFactory.criar_categoria(
            id=categoria_dados['id'],
            nome=categoria_dados['nome'],
            descricao=categoria_dados['descricao']
        )

        promocao_dados = self.__dao_promocoes.pegar_promocao_por_id(promocao_id)

        if custo_entrada <= 10 and promocao_dados:
            flash('Você não pode definir uma promocão para um ponto abaixo de R$10.', 'danger')
            return redirect(url_for('pontos.editar_ponto', id=id_ponto))

        if promocao_dados:

            promocao = PromocaoFactory.criar_promocao(
                id=promocao_dados.id,
                titulo=promocao_dados.titulo,
                data_inicio=promocao_dados.data_inicio,
                data_fim=promocao_dados.data_fim,
                desconto=promocao_dados.desconto
            )
        else:
            promocao = None

        if tipo_ponto == "cultural":
            tipo_cultural_dados = self.__dao_tipo_cultural.buscar_tipo_por_id(tipo_cultural_id)

            if not tipo_cultural_dados:
                flash('Tipo cultural selecionado não encontrado.', 'danger')
                return redirect(url_for('pontos.editar_ponto', id=id_ponto))

            tipo_cultural = TipoCulturalFactory.criar_tipo_cultural(
                id=tipo_cultural_dados.id,
                nome=tipo_cultural_dados.nome
            )

            ponto_atualizado = PontoTuristicoFactory.criar_ponto_turistico(
                id=id_ponto,
                nome=nome.capitalize().strip(),
                localizacao=localizacao.capitalize().strip(),
                descricao=descricao.capitalize().strip(),
                horario_funcionamento=horario_funcionamento.capitalize().strip(),
                custo_entrada=custo_entrada,
                categoria=categoria,
                promocao=promocao,
                url_imagem=nome_arquivo,
                tipo_cultural=tipo_cultural,
                ano_fundacao=ano_fundacao.strip() if ano_fundacao else "Não informado",
                status=ponto_existente.status,
                tipo_ponto=tipo_ponto
            )
        else:
            ecossistema_dados = self.__dao_ecossistema.buscar_ecossistema_por_id(ecossistema_id)

            if not ecossistema_dados:
                flash('Ecossistema selecionado não encontrado.', 'danger')
                return redirect(url_for('pontos.editar_ponto', id=id_ponto))

            ecossistema = EcossistemaFactory.criar_ecossistema(
                id=ecossistema_dados.id,
                nome=ecossistema_dados.nome
            )

            ponto_atualizado = PontoTuristicoFactory.criar_ponto_turistico(
                id=id_ponto,
                nome=nome.capitalize().strip(),
                localizacao=localizacao.capitalize().strip(),
                descricao=descricao.capitalize().strip(),
                horario_funcionamento=horario_funcionamento.capitalize().strip(),
                custo_entrada=custo_entrada,
                categoria=categoria,
                promocao=promocao,
                url_imagem=nome_arquivo,
                tipo_ponto=tipo_ponto,
                ecossistema=ecossistema,
                area_km=area_km if area_km else 0,
                status=ponto_existente.status
            )

        imagem_antiga = ponto_existente.url_imagem

        self.__dao_pontos.atualizar_ponto(ponto_atualizado, imagem_antiga)

        flash('Ponto turístico atualizado com sucesso!', 'success')
        return self.preparar_gerenciar_pontos()
    
    def listar_pontos_busca(self):
        escrita = request.form.get('escrita')
        filtro = request.form.get('filtro')

        if not escrita or not filtro:
            flash('Para pesquisar um ponto turístico é necessário informar o filtro e a escrita', 'danger')
            return redirect(url_for('pontos.index'))

        if escrita:
            escrita = escrita.capitalize().strip()

        lista_pontos = self.__dao_pontos.buscar_pontos(escrita, filtro)

        if session.get('usuario'):
            usuario_email = session['usuario']['email']
            usuario = self.__dao_usuario.buscar_usuario_por_email(usuario_email)

            favoritos_ids = [ponto.id for ponto in usuario.pontos_favoritos]
        else:
            favoritos_ids = []

        return render_template('pontos_busca.html', lista_pontos=lista_pontos, favoritos_ids=favoritos_ids)