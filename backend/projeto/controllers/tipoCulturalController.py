from flask import render_template, request, jsonify
from projeto.dao import TipoCulturalDAO
from projeto.factorys import TipoCulturalFactory
from projeto.decoradores import admin_required

class TipoCulturalController:

    def __init__(self):
        self.__dao = TipoCulturalDAO()

    def listar_tipos_culturais(self):
        lista = self.__dao.carregar_tipos_culturais()
        tipos_culturais = []

        for obj in lista:
            tipos_culturais.append(obj.to_dict())

        return jsonify(tipos_culturais), 200

    def preparar_gerenciar_tipos(self):
        return render_template('tipo_cultural/gerenciar_tipos_culturais.html')

    @admin_required
    def cadastrar_tipo_cultural(self, usuario):
        dados = request.get_json()
        nome = dados.get('nome')

        nomes_tipos = self.__dao.pegar_nomes_tipos_culturais()

        if not nome:
            return jsonify({'mensagem': 'O campo nome do tipo cultural é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_tipos:
            return jsonify({'mensagem': 'Já existe um tipo cultural com esse nome.', 'classe': 'danger'}), 409

        novo_tipo = TipoCulturalFactory.criar_tipo_cultural(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_tipo_cultural(novo_tipo)

        return jsonify({'mensagem': 'Tipo cultural cadastrado com sucesso!', 'classe': 'success'}), 201

    @admin_required
    def remover_tipo_cultural(self, usuario, id_tipo):
        self.__dao.remover_tipo_cultural(id_tipo)

        return jsonify({'mensagem': 'Tipo cultural removido com sucesso!', 'classe': 'success'}), 200

    def preparar_editar_tipo(self, id_tipo):
        return render_template('tipo_cultural/editar_tipo_cultural.html')

    @admin_required
    def buscar_tipo_cultural_por_id(self, usuario, id_tipo):
        tipo = self.__dao.buscar_tipo_por_id(id_tipo)

        if not tipo:
            return jsonify({'mensagem': 'Tipo cultural não encontrado.', 'classe': 'danger'}), 404

        return jsonify(tipo.to_dict()), 200

    @admin_required
    def atualizar_tipo_cultural(self, usuario, id_tipo):
        dados = request.get_json()
        nome = dados.get('nome')

        nomes_tipos = self.__dao.pegar_nomes_tipos_culturais()

        tipo_atual = self.__dao.buscar_tipo_por_id(id_tipo)

        if not nome:
            return jsonify({'mensagem': 'O campo nome do tipo cultural é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_tipos and nome.capitalize().strip() != tipo_atual.nome:
            return jsonify({'mensagem': 'Já existe um tipo cultural com esse nome.', 'classe': 'danger'}), 409

        tipo_atualizado = TipoCulturalFactory.criar_tipo_cultural(
            nome=nome.capitalize().strip(),
            id=id_tipo
        )

        self.__dao.atualizar_tipo_cultural(tipo_atualizado)

        return jsonify({'mensagem': 'Tipo cultural atualizado com sucesso!', 'classe': 'success'}), 200