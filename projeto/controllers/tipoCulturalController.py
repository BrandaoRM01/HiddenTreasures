from flask import flash, render_template, redirect, session, url_for, request, jsonify
from projeto.dao import TipoCulturalDAO
from projeto.factorys import TipoCulturalFactory

class TipoCulturalController:

    def __init__(self):
        self.__dao = TipoCulturalDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def listar_tipos_culturais(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        lista = self.__dao.carregar_tipos_culturais()
        tipos_culturais = []

        for obj in lista:
            tipos_culturais.append(obj.to_dict())

        return jsonify(tipos_culturais), 200

    def preparar_gerenciar_tipos(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return render_template('tipo_cultural/gerenciar_tipos_culturais.html')

    def cadastrar_tipo_cultural(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        dados = request.get_json()
        nome = dados.get('nome')

        nomes_tipos = self.__dao.pegar_nomes_tipos_culturais()

        if not nome:
            return jsonify({'mensagem': 'O campo nome do tipo cultural é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_tipos:
            return jsonify({'mensagem': 'Já existe um tipo cultural com esse nome.', 'classe': 'danger'}), 400

        novo_tipo = TipoCulturalFactory.criar_tipo_cultural(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_tipo_cultural(novo_tipo)

        return jsonify({'mensagem': 'Tipo cultural cadastrado com sucesso!', 'classe': 'success'}), 200

    def remover_tipo_cultural(self, id_tipo):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        self.__dao.remover_tipo_cultural(id_tipo)

        return jsonify({'mensagem': 'Tipo cultural removido com sucesso!', 'classe': 'success'}), 200

    def preparar_editar_tipo(self, id_tipo):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return render_template('tipo_cultural/editar_tipo_cultural.html')

    def buscar_tipo_cultural_por_id(self, id_tipo):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        tipo = self.__dao.buscar_tipo_por_id(id_tipo)

        if not tipo:
            return jsonify({'mensagem': 'Tipo cultural não encontrado.', 'classe': 'danger'}), 400

        return jsonify(tipo.to_dict()), 200

    def atualizar_tipo_cultural(self, id_tipo):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        dados = request.get_json()
        nome = dados.get('nome')

        nomes_tipos = self.__dao.pegar_nomes_tipos_culturais()

        tipo_atual = self.__dao.buscar_tipo_por_id(id_tipo)

        if not nome:
            return jsonify({'mensagem': 'O campo nome do tipo cultural é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_tipos and nome.capitalize().strip() != tipo_atual.nome:
            return jsonify({'mensagem': 'Já existe um tipo cultural com esse nome.', 'classe': 'danger'}), 400

        tipo_atualizado = TipoCulturalFactory.criar_tipo_cultural(
            nome=nome.capitalize().strip(),
            id=id_tipo
        )

        self.__dao.atualizar_tipo_cultural(tipo_atualizado)

        return jsonify({'mensagem': 'Tipo cultural atualizado com sucesso!', 'classe': 'success'}), 200