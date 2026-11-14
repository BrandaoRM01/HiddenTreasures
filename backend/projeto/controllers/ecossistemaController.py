from flask import render_template, request, jsonify
from projeto.dao import EcossistemaDAO
from projeto.factorys import EcossistemaFactory
from projeto.decoradores import admin_required

class EcossistemaController:

    def __init__(self):
        self.__dao = EcossistemaDAO()

    def listar_ecossistemas(self):
        lista = self.__dao.carregar_ecossistemas()
        ecossistemas = []

        for obj in lista:
            ecossistemas.append(obj.to_dict())

        return jsonify(ecossistemas), 200

    def preparar_gerenciar_ecossistemas(self):
        return render_template('ecossistema/gerenciar_ecossistemas.html')

    @admin_required
    def cadastrar_ecossistema(self, usuario):
        dados = request.get_json()
        nome = dados.get('nome')

        nomes_ecossistemas = self.__dao.pegar_nomes_ecossistemas()

        if not nome:
            return jsonify({'mensagem': 'O campo nome do ecossistema é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_ecossistemas:
            return jsonify({'mensagem': 'Já existe um ecossistema com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 409

        novo_ecossistema = EcossistemaFactory.criar_ecossistema(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_ecossistema(novo_ecossistema)

        return jsonify({'mensagem': 'Ecossistema cadastrado com sucesso!', 'classe': 'success'}), 201

    @admin_required
    def remover_ecossistema(self, usuario, id_ecossistema):
        self.__dao.remover_ecossistema(id_ecossistema)

        return jsonify({'mensagem': 'Ecossistema removido com sucesso!', 'classe': 'success'}), 200

    def preparar_editar_ecossistema(self, id_ecossistema):
        return render_template('ecossistema/editar_ecossistema.html')

    @admin_required
    def buscar_ecossistema_por_id(self, usuario, id):
        ecossistema = self.__dao.buscar_ecossistema_por_id(id)

        if not ecossistema:
            return jsonify({'mensagem': 'Ecossistema não encontrado.', 'classe': 'danger'}), 404

        return jsonify(ecossistema.to_dict()), 200

    @admin_required
    def atualizar_ecossistema(self, usuario, id_ecossistema):
        dados = request.get_json()
        nome = dados.get('nome')

        nomes_ecossistemas = self.__dao.pegar_nomes_ecossistemas()

        ecossistema_atual = self.__dao.buscar_ecossistema_por_id(id_ecossistema)

        if not nome:
            return jsonify({'mensagem': 'O campo nome do ecossistema é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_ecossistemas and nome.capitalize().strip() != ecossistema_atual.nome:
            return jsonify({'mensagem': 'Já existe um ecossistema com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 409

        ecossistema_atualizado = EcossistemaFactory.criar_ecossistema(
            nome=nome.capitalize().strip(),
            id=id_ecossistema
        )

        self.__dao.atualizar_ecossistema(ecossistema_atualizado)

        return jsonify({'mensagem': 'Ecossistema atualizado com sucesso!', 'classe': 'success'}), 200