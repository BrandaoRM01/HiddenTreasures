from flask import render_template, redirect, url_for, request, session, jsonify
from projeto.dao import PontoTuristicoDAO, CategoriaDAO, UserDAO, PromocaoDAO, TipoCulturalDAO, EcossistemaDAO, DestaqueDAO
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
        self.__dao_destaque = DestaqueDAO()

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
   
        return render_template('ponto_turistico/index.html', pontos_promocao=pontos_promocao, top_pontos=top_pontos, favoritos_ids=favoritos_ids)

    def preparar_sobre(self):
        return render_template('ponto_turistico/sobre.html')

    def preparar_gerenciar_pontos(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return render_template('ponto_turistico/gerenciar_pontos.html')

    def listar_pontos_gerenciar(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        lista = self.__dao_pontos.listar_todos_pontos()
        pontos = [obj.to_dict() for obj in lista]

        return jsonify(pontos), 200

    def preparar_gerenciar_sugestoes(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return render_template('ponto_turistico/gerenciar_sugestoes.html')

    def listar_sugestoes(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        lista = self.__dao_pontos.listar_pontos_sugeridos()
        sugestoes = [obj.to_dict() for obj in lista]

        return jsonify(sugestoes), 200
    
    def preparar_sugerir_ponto(self):
        if 'usuario' not in session:
            return render_template('erro.html')
        
        if self.__usuario_pode_moderar():
            return redirect(url_for('pontos.gerenciar_pontos'))

        return render_template('ponto_turistico/sugerir_ponto.html')

    def listar_sugestoes_usuario(self):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        lista = self.__dao_pontos.listar_sugestoes_usuario(session['usuario']['email'])
        sugestoes = [obj.to_dict() for obj in lista]

        return jsonify(sugestoes), 200

    def preparar_editar_ponto(self, id_ponto):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            return render_template('erro.html')

        if ponto.sugerido_por:
            return redirect(url_for('pontos.editar_sugestao', id=id_ponto))

        return render_template('ponto_turistico/editar_ponto.html')
    
    def preparar_editar_sugestao(self, id_ponto):
        if 'usuario' not in session:
            return render_template('erro.html')
        
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            return render_template('erro.html')

        if session['usuario']['email'] != ponto.sugerido_por:
            if not session['usuario']['pode_moderar']:
                return redirect(url_for('pontos.sugerir_ponto'))
            else:
                return redirect(url_for('pontos.gerenciar_sugestoes'))
            
        if session['usuario']['email'] == ponto.sugerido_por and ponto.status == 'aprovado':
            return redirect(url_for('pontos.sugerir_ponto'))

        return render_template('ponto_turistico/editar_sugestao.html')

    def buscar_ponto(self, id_ponto):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 400

        return jsonify(ponto.to_dict()), 200

    def preparar_pontos_turisticos(self):
        return render_template('ponto_turistico/pontos.html')

    def listar_pontos_aprovados(self):
        lista = self.__dao_pontos.listar_pontos()

        if session.get('usuario'):
            usuario_email = session['usuario']['email']
            usuario = self.__dao_usuario.buscar_usuario_por_email(usuario_email)

            favoritos_ids = [ponto.id for ponto in usuario.pontos_favoritos]
        else:
            favoritos_ids = []

        pontos = []

        for p in lista:
            ponto = p.to_dict()
            ponto['favorito'] = p.id in favoritos_ids
            pontos.append(ponto)

        return jsonify({'logado': bool(session.get('usuario')), 'pontos': pontos}), 200

    def preparar_detalhes_ponto(self, id_ponto):
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)
        usuario_email = None
        avaliacao_usuario = None

        if not ponto:
            return redirect(url_for('pontos.pontos'))
        
        if 'usuario' in session:
            usuario_email = session['usuario']['email']

        for avaliacao in ponto.avaliacoes:
            if usuario_email and avaliacao.usuario.email == usuario_email:
                avaliacao_usuario = avaliacao
                break

        ultimas_avaliacoes = ponto.avaliacoes[-5:]

        return render_template('ponto_turistico/detalhes_ponto.html', ponto=ponto, avaliacoes=ultimas_avaliacoes, avaliacao_usuario=avaliacao_usuario, quantidade=len(ponto.avaliacoes))
    
    def cadastrar_ponto(self):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        
        if not session['usuario']['pode_moderar']:
            status = 'pendente'
            sugerido_por = session['usuario']['email']
        else:
            status = 'aprovado'
            sugerido_por = None
        
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
        destaques_ids = request.form.getlist('destaques')   

        if not nome or not localizacao or not descricao or not categoria_id:
            return jsonify({'mensagem': 'Por favor, preencha todos os campos obrigatórios.', 'classe': 'danger'}), 400

        nomes_pontos = self.__dao_pontos.buscar_nomes_pontos()

        if nome.capitalize().strip() in nomes_pontos:
            return jsonify({'mensagem': 'Nome já cadastrado no sistema, tente outro!', 'classe': 'danger'}), 400
        
        if not custo_entrada:
            custo_entrada = 0.0
        else:
            try:
                custo_entrada = float(custo_entrada)
            except (ValueError, TypeError):
                return jsonify({'mensagem': 'Por favor, insira um valor válido para o custo de entrada.', 'classe': 'danger'}), 400
            
        if tipo_ponto == 'natural':
            if not area_km:
                area_km = 0.0
            else:
                try:
                    area_km = float(area_km)
                except (ValueError, TypeError):
                    return jsonify({'mensagem': 'Por favor, insira um valor válido para a área.', 'classe': 'danger'}), 400
            
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
            return jsonify({'mensagem': 'Categoria selecionada não encontrada.', 'classe': 'danger'}), 400
        
        categoria = CategoriaFactory.criar_categoria(
            id=categoria_dados['id'],
            nome=categoria_dados['nome'],
            descricao=categoria_dados['descricao']
        )

        promocao_dados = self.__dao_promocoes.pegar_promocao_por_id(promocao_id)

        if custo_entrada <= 10 and promocao_dados:
            return jsonify({'mensagem': 'Você não pode definir uma promocão para um ponto abaixo de R$10.', 'classe': 'danger'}), 400

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

            if tipo_cultural_dados:
                tipo_cultural = TipoCulturalFactory.criar_tipo_cultural(
                    id=tipo_cultural_dados.id,
                    nome=tipo_cultural_dados.nome
                )
            else:
                tipo_cultural = None

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
                status=status,
                tipo_ponto=tipo_ponto,
                sugerido_por=sugerido_por
            )
        else:
            ecossistema_dados = self.__dao_ecossistema.buscar_ecossistema_por_id(ecossistema_id)

            if ecossistema_dados:
                ecossistema = EcossistemaFactory.criar_ecossistema(
                    id=ecossistema_dados.id,
                    nome=ecossistema_dados.nome
                )
            else:
                ecossistema = None

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
                status=status,
                sugerido_por=sugerido_por
            )

        self.__dao_pontos.cadastrar_ponto(novo_ponto, destaques_ids)

        return jsonify({'mensagem': 'Ponto turístico cadastrado com sucesso!', 'classe': 'success'}), 200
    
    def remover_ponto(self, id_ponto):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 400

        if not session['usuario']['pode_moderar'] and session['usuario']['email'] == ponto.sugerido_por and ponto.status == 'aprovado':
            return jsonify({'mensagem': 'Você não pode excluir sua sugestão porque ela já foi aprovada!', 'classe': 'danger'}), 400

        self.__dao_pontos.excluir_ponto(id_ponto)

        return jsonify({'mensagem': 'Ponto turístico excluído com sucesso!', 'classe': 'success'}), 200
    
    def editar_ponto(self, id_ponto):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
    
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
        destaques_ids = request.form.getlist('destaques')

        if not nome or not localizacao or not descricao or not categoria_id:
            return jsonify({'mensagem': 'Por favor, preencha todos os campos obrigatórios.', 'classe': 'danger'}), 400
      
        if not custo_entrada:
            custo_entrada = 0.0
        else:
            try:
                custo_entrada = float(custo_entrada)
            except (ValueError, TypeError):
                return jsonify({'mensagem': 'Por favor, insira um valor válido para o custo de entrada.', 'classe': 'danger'}), 400
            
        if tipo_ponto == 'natural':
            if not area_km:
                area_km = 0.0
            else:
                try:
                    area_km = float(area_km)
                except (ValueError, TypeError):
                    return jsonify({'mensagem': 'Por favor, insira um valor válido para a área.', 'classe': 'danger'}), 400
            
        if not horario_funcionamento:
            horario_funcionamento = "Não informado"

        ponto_existente = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto_existente:
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 400

        nomes_pontos = self.__dao_pontos.buscar_nomes_pontos()
        nome_atual = ponto_existente.nome

        if nome.capitalize().strip() in nomes_pontos and nome.capitalize().strip() != nome_atual:
            return jsonify({'mensagem': 'Nome já cadastrado no sistema, tente outro!', 'classe': 'danger'}), 400

        if not session['usuario']['pode_moderar']:
            ponto_existente.status = 'pendente'

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
            return jsonify({'mensagem': 'Categoria selecionada não encontrada.', 'classe': 'danger'}), 400

        categoria = CategoriaFactory.criar_categoria(
            id=categoria_dados['id'],
            nome=categoria_dados['nome'],
            descricao=categoria_dados['descricao']
        )

        promocao_dados = self.__dao_promocoes.pegar_promocao_por_id(promocao_id)

        if custo_entrada <= 10 and promocao_dados:
            return jsonify({'mensagem': 'Você não pode definir uma promocão para um ponto abaixo de R$10.', 'classe': 'danger'}), 400

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

            if tipo_cultural_dados:
                tipo_cultural = TipoCulturalFactory.criar_tipo_cultural(
                    id=tipo_cultural_dados.id,
                    nome=tipo_cultural_dados.nome
                )
            else:
                tipo_cultural = None

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
                tipo_ponto=tipo_ponto,
                sugerido_por=ponto_existente.sugerido_por
            )
        else:
            ecossistema_dados = self.__dao_ecossistema.buscar_ecossistema_por_id(ecossistema_id)

            if ecossistema_dados:
                ecossistema = EcossistemaFactory.criar_ecossistema(
                    id=ecossistema_dados.id,
                    nome=ecossistema_dados.nome
                )
            else:
                ecossistema = None

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
                status=ponto_existente.status,
                sugerido_por=ponto_existente.sugerido_por
            )

        imagem_antiga = ponto_existente.url_imagem

        self.__dao_pontos.atualizar_ponto(ponto_atualizado, imagem_antiga, destaques_ids)

        return jsonify({'mensagem': 'Ponto turístico atualizado com sucesso!', 'classe': 'success'}), 200
        
    def listar_pontos_busca(self):
        escrita = request.form.get('escrita')
        filtro = request.form.get('filtro')

        if not escrita or not filtro:
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

        return render_template('ponto_turistico/pontos_busca.html', lista_pontos=lista_pontos, favoritos_ids=favoritos_ids)
    
    def alterar_status(self, id_ponto, status):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        if status not in ['aprovado', 'rejeitado']:
            return jsonify({'mensagem': 'Status inválido. Informe um status válido.', 'classe': 'danger'}), 400

        self.__dao_pontos.alterar_status(id_ponto, status)

        return jsonify({'mensagem': f'Sugestão alterada com sucesso para o status de {status}!', 'classe': 'success'}), 200