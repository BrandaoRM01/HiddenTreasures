from flask import render_template, request, jsonify
from projeto.dao import DestaqueDAO
from projeto.factorys import DestaqueFactory
from projeto.decoradores import admin_required

class DestaqueController:

    def __init__(self):
        self.__dao = DestaqueDAO()

    def listar_destaques(self):
        lista = self.__dao.carregar_destaques()
        destaques = []

        for obj in lista:
            destaques.append(obj.to_dict())

        return jsonify(destaques), 200

    def preparar_gerenciar_destaques(self):
        return render_template('destaque/gerenciar_destaques.html')

    @admin_required
    def cadastrar_destaque(self, usuario):
        dados = request.get_json()
        nome = dados.get('nome')

        nomes_destaques = self.__dao.pegar_nomes_destaques()

        if not nome:
            return jsonify({'mensagem': 'O campo nome do destaque é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_destaques:
            return jsonify({'mensagem': 'Já existe um destaque com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 400

        novo_destaque = DestaqueFactory.criar_destaque(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_destaque(novo_destaque)

        return jsonify({'mensagem': 'Destaque cadastrado com sucesso!', 'classe': 'success'}), 200

    @admin_required
    def remover_destaque(self, usuario, id_destaque):
        self.__dao.remover_destaque(id_destaque)

        return jsonify({'mensagem': 'Destaque removido com sucesso!', 'classe': 'success'}), 200

    def preparar_editar_destaque(self, id_destaque):
        return render_template('destaque/editar_destaque.html')

    @admin_required
    def buscar_destaque_por_id(self, usuario, id):
        destaque = self.__dao.buscar_destaque_por_id(id)

        if not destaque:
            return jsonify({'mensagem': 'Destaque não encontrado.', 'classe': 'danger'}), 400

        return jsonify(destaque.to_dict()), 200

    @admin_required
    def atualizar_destaque(self, usuario, id_destaque):
        dados = request.get_json()
        nome = dados.get('nome')

        nomes_destaques = self.__dao.pegar_nomes_destaques()

        destaque_atual = self.__dao.buscar_destaque_por_id(id_destaque)

        if not nome:
            return jsonify({'mensagem': 'O campo nome do destaque é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_destaques and nome.capitalize().strip() != destaque_atual.nome:
            return jsonify({'mensagem': 'Já existe um destaque com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 400

        destaque_atualizado = DestaqueFactory.criar_destaque(
            id=id_destaque,
            nome=nome.capitalize().strip()
        )

        self.__dao.atualizar_destaque(destaque_atualizado)

        return jsonify({'mensagem': 'Destaque atualizado com sucesso!', 'classe': 'success'}), 200