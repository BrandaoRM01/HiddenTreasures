from flask import request, session, jsonify, render_template
from projeto.dao import AvaliacaoDAO, UserDAO, PontoTuristicoDAO
from projeto.factorys import AvaliacaoFactory
from datetime import datetime

class AvaliacaoController:

    def __init__(self):
        self.__dao_avaliacao = AvaliacaoDAO()
        self.__dao_ponto = PontoTuristicoDAO()
        self.__dao_user = UserDAO()

    def preparar_avaliacoes_ponto(self, ponto_id):
        ponto = self.__dao_ponto.buscar_ponto_por_id(ponto_id)

        if not ponto:
            return render_template('erro.html')

        return render_template('avaliacao/avaliacoes_ponto.html')

    def preparar_editar_avaliacao(self, ponto_id):
        if 'usuario' not in session:
            return render_template('erro.html')

        usuario_email = session['usuario']['email']
        avaliacao = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)

        if not avaliacao:
            return render_template('erro.html')

        return render_template('avaliacao/editar_avaliacao.html')

    def listar_avaliacoes_ponto(self, ponto_id):
        ponto = self.__dao_ponto.buscar_ponto_por_id(ponto_id)

        if not ponto:
            return jsonify({'mensagem': 'Ponto turístico não encontrado.', 'classe': 'danger'}), 400

        usuario_email = None
        avaliacao_usuario = None
        logado = 'usuario' in session
        usuario_admin = False

        if logado:
            usuario_email = session['usuario']['email']
            usuario_admin = session['usuario']['tipo_usuario'] in ['admin', 'superadmin']

            avaliacao_usuario_obj = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)
            if avaliacao_usuario_obj:
                avaliacao_usuario = avaliacao_usuario_obj.to_dict()

        avaliacoes = self.__dao_avaliacao.listar_avaliacoes_por_ponto(ponto_id, usuario_email)
        avaliacoes_json = [avaliacao.to_dict() for avaliacao in avaliacoes]

        dados = {
            'logado': logado,
            'usuario_admin': usuario_admin,
            'ponto_nome': ponto.nome,
            'avaliacoes': avaliacoes_json,
            'avaliacao_usuario': avaliacao_usuario
        }
        
        return jsonify(dados), 200

    def cadastrar_avaliacao(self, ponto_id):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        usuario_email = session['usuario']['email']

        dados = request.get_json()
        nota = dados.get('nota')
        comentario = dados.get('comentario')

        usuario = self.__dao_user.buscar_usuario_por_email(usuario_email)
        ponto = self.__dao_ponto.buscar_ponto_por_id(ponto_id)

        if not usuario or not ponto:
            return jsonify({'mensagem': 'Usuário ou ponto turístico não encontrado.', 'classe': 'danger'}), 400

        avaliacao_existente = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)

        if avaliacao_existente:
            return jsonify({'mensagem': 'Você já avaliou este ponto turístico. Edite a avaliação existente ou remova-a antes de criar uma nova.', 'classe': 'danger'}), 400

        if not nota:
            return jsonify({'mensagem': 'A nota é obrigatória para cadastrar uma avaliação.', 'classe': 'danger'}), 400

        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                return jsonify({'mensagem': 'A nota deve ser um número inteiro entre 1 e 5.', 'classe': 'danger'}), 400
        except (ValueError, TypeError):
            return jsonify({'mensagem': 'A nota deve ser um número inteiro entre 1 e 5.', 'classe': 'danger'}), 400

        if comentario:
            comentario = comentario.strip().capitalize()

        nova_avaliacao = AvaliacaoFactory.criar_avaliacao(
            usuario=usuario,
            ponto_id=ponto_id,
            nota=nota,
            data_avaliacao=datetime.now(),
            comentario=comentario
        )

        self.__dao_avaliacao.cadastrar_avaliacao(nova_avaliacao)

        return jsonify({'mensagem': 'Avaliação cadastrada com sucesso!', 'classe': 'success'}), 200

    def atualizar_avaliacao(self, ponto_id):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        usuario_email = session['usuario']['email']

        dados = request.get_json()
        nota = dados.get('nota')
        comentario = dados.get('comentario')

        avaliacao = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)

        if not avaliacao:
            return jsonify({'mensagem': 'Avaliação não encontrada.', 'classe': 'danger'}), 400

        if not nota:
            return jsonify({'mensagem': 'A nota é obrigatória para atualizar a avaliação.', 'classe': 'danger'}), 400

        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                return jsonify({'mensagem': 'A nota deve ser um número inteiro entre 1 e 5.', 'classe': 'danger'}), 400
        except (ValueError, TypeError):
            return jsonify({'mensagem': 'A nota deve ser um número inteiro entre 1 e 5.', 'classe': 'danger'}), 400

        if comentario:
            comentario = comentario.strip().capitalize()

        avaliacao_atualizada = AvaliacaoFactory.criar_avaliacao(
            usuario=avaliacao.usuario,
            ponto_id=avaliacao.ponto_id,
            nota=nota,
            data_avaliacao=avaliacao.data_avaliacao,
            comentario=comentario
        )

        self.__dao_avaliacao.atualizar_avaliacao(avaliacao_atualizada)

        return jsonify({'mensagem': 'Avaliação atualizada com sucesso!', 'classe': 'success'}), 200

    def remover_avaliacao(self, ponto_id):
        if 'usuario' not in session:
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        usuario_email_atual = session['usuario']['email']
        tipo_usuario = session['usuario']['tipo_usuario']

        usuario_email = request.args.get('usuario_email') or usuario_email_atual

        if usuario_email != usuario_email_atual and tipo_usuario not in ['admin', 'superadmin']:
            return jsonify({'mensagem': 'Você só pode remover sua própria avaliação.', 'classe': 'danger'}), 403

        avaliacao = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)

        if not avaliacao:
            return jsonify({'mensagem': 'Avaliação não encontrada.', 'classe': 'danger'}), 400

        self.__dao_avaliacao.remover_avaliacao(usuario_email, ponto_id)

        return jsonify({'mensagem': 'Avaliação removida com sucesso!', 'classe': 'success'}), 200