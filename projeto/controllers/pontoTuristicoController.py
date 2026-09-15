from flask import render_template, redirect, url_for, request, jsonify
from projeto.dao import PontoTuristicoDAO, CategoriaDAO, UserDAO, PromocaoDAO, TipoCulturalDAO, EcossistemaDAO, DestaqueDAO
from projeto.factorys import PontoTuristicoFactory, CategoriaFactory, PromocaoFactory, TipoCulturalFactory, EcossistemaFactory
from projeto.config import Config
from projeto.decoradores import login_required, admin_required, usuario_opcional
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

    def __status_valido(self, status):
        return status in ['aprovado', 'rejeitado', 'pendente']

    def preparar_erro(self):
        return render_template('erro.html')

    def preparar_index(self):
        return render_template('ponto_turistico/index.html')

    @usuario_opcional
    def listar_pontos(self, usuario):
        busca = request.args.get('busca')
        categoria = request.args.get('categoria')
        tipo = request.args.get('tipo')
        localizacao = request.args.get('localizacao')
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)

        eh_admin = bool(usuario) and usuario.pode_moderar()

        if eh_admin:
            if status and not self.__status_valido(status):
                return jsonify({'mensagem': 'Status inválido.', 'classe': 'danger'}), 400
            status_filtro = status       
            apenas_aprovados = False
        else:
            status_filtro = None
            apenas_aprovados = True         

        lista, total, page, limit = self.__dao_pontos.listar_pontos_busca(
            busca=busca,
            categoria=categoria,
            tipo=tipo,
            localizacao=localizacao,
            status=status_filtro,
            apenas_aprovados=apenas_aprovados,
            page=page,
            limit=limit
        )

        if usuario:
            favoritos_ids = [p.id for p in usuario.pontos_favoritos]
        else:
            favoritos_ids = []

        pontos = []
        for p in lista:
            ponto = p.to_dict()
            ponto['favorito'] = p.id in favoritos_ids
            pontos.append(ponto)

        return jsonify({
            'logado': bool(usuario),
            'pontos': pontos,
            'paginacao': {
                'page': page,
                'limit': limit,
                'total': total,
                'total_paginas': (total + limit - 1) // limit
            }
        }), 200

    @usuario_opcional
    def listar_index(self, usuario):
        top_pontos = self.__dao_pontos.listar_top_pontos()
        pontos = self.__dao_pontos.listar_pontos()

        pontos_promocao = []

        if pontos:
            for ponto in pontos:
                if ponto.promocao is not None:
                    pontos_promocao.append(ponto)

        if usuario:
            favoritos_ids = [ponto.id for ponto in usuario.pontos_favoritos]
        else:
            favoritos_ids = []

        top_pontos_json = []
        for p in (top_pontos or []):
            ponto = p.to_dict()
            ponto['favorito'] = p.id in favoritos_ids
            top_pontos_json.append(ponto)

        pontos_promocao_json = []
        for p in pontos_promocao:
            ponto = p.to_dict()
            ponto['favorito'] = p.id in favoritos_ids
            pontos_promocao_json.append(ponto)

        dados = {
            'logado': bool(usuario),
            'top_pontos': top_pontos_json,
            'pontos_promocao': pontos_promocao_json
        }

        return jsonify(dados), 200

    def preparar_sobre(self):
        return render_template('ponto_turistico/sobre.html')

    def preparar_gerenciar_pontos(self):
        return render_template('ponto_turistico/gerenciar_pontos.html')

    def preparar_gerenciar_sugestoes(self):
        return render_template('ponto_turistico/gerenciar_sugestoes.html')

    @admin_required
    def listar_sugestoes(self, usuario):
        lista = self.__dao_pontos.listar_pontos_sugeridos()
        sugestoes = [obj.to_dict() for obj in lista]

        return jsonify(sugestoes), 200

    def preparar_sugerir_ponto(self):
        return render_template('ponto_turistico/sugerir_ponto.html')

    @login_required
    def listar_sugestoes_usuario(self, usuario):
        lista = self.__dao_pontos.listar_sugestoes_usuario(usuario.email)
        sugestoes = [obj.to_dict() for obj in lista]

        return jsonify(sugestoes), 200

    def preparar_editar_ponto(self, id_ponto):
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if ponto and ponto.sugerido_por:
            return redirect(url_for('pontos.editar_sugestao', id=id_ponto))

        return render_template('ponto_turistico/editar_ponto.html')

    def preparar_editar_sugestao(self, id_ponto):
        return render_template('ponto_turistico/editar_sugestao.html')

    @login_required
    def buscar_ponto(self, usuario, id_ponto):
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 404

        return jsonify(ponto.to_dict()), 200

    def preparar_pontos_turisticos(self):
        return render_template('ponto_turistico/pontos.html')

    def preparar_detalhes_ponto(self):
        return render_template('ponto_turistico/detalhes_ponto.html')

    @usuario_opcional
    def detalhes_ponto_api(self, usuario, id_ponto):
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 404

        favorito = False
        if usuario:
            favorito = any(p.id == ponto.id for p in usuario.pontos_favoritos)

        dados = ponto.to_dict()
        dados['favorito'] = favorito
        dados['logado'] = bool(usuario)

        return jsonify(dados), 200

    @login_required
    def cadastrar_ponto(self, usuario):
        if not usuario.pode_moderar():
            status = 'pendente'
            sugerido_por = usuario.email
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
            return jsonify({'mensagem': 'Nome já cadastrado no sistema, tente outro!', 'classe': 'danger'}), 409

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
            return jsonify({'mensagem': 'Categoria selecionada não encontrada.', 'classe': 'danger'}), 404

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

        return jsonify({'mensagem': 'Ponto turístico cadastrado com sucesso!', 'classe': 'success'}), 201

    @login_required
    def remover_ponto(self, usuario, id_ponto):
        ponto = self.__dao_pontos.buscar_ponto_por_id(id_ponto)

        if not ponto:
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 404

        if not usuario.pode_moderar() and usuario.email == ponto.sugerido_por and ponto.status == 'aprovado':
            return jsonify({'mensagem': 'Você não pode excluir sua sugestão porque ela já foi aprovada!', 'classe': 'danger'}), 403

        self.__dao_pontos.excluir_ponto(id_ponto)

        return jsonify({'mensagem': 'Ponto turístico excluído com sucesso!', 'classe': 'success'}), 204

    @login_required
    def editar_ponto(self, usuario, id_ponto):
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
        status_recebido = request.form.get('status')

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
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 404

        nomes_pontos = self.__dao_pontos.buscar_nomes_pontos()
        nome_atual = ponto_existente.nome

        if nome.capitalize().strip() in nomes_pontos and nome.capitalize().strip() != nome_atual:
            return jsonify({'mensagem': 'Nome já cadastrado no sistema, tente outro!', 'classe': 'danger'}), 409

        if not usuario.pode_moderar():
            ponto_existente.status = 'pendente'
        elif status_recebido:
            if not self.__status_valido(status_recebido):
                return jsonify({'mensagem': 'Status inválido. Informe um status válido.', 'classe': 'danger'}), 400
            ponto_existente.status = status_recebido

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
            return jsonify({'mensagem': 'Categoria selecionada não encontrada.', 'classe': 'danger'}), 404

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

    @admin_required
    def alterar_status(self, usuario, id_ponto, status):
        if status not in ['aprovado', 'rejeitado']:
            return jsonify({'mensagem': 'Status inválido. Informe um status válido.', 'classe': 'danger'}), 400

        self.__dao_pontos.alterar_status(id_ponto, status)

        return jsonify({'mensagem': f'Sugestão alterada com sucesso para o status de {status}!', 'classe': 'success'}), 200