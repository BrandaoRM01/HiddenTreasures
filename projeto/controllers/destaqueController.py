from flask import flash, render_template, redirect, session, url_for, request, jsonify
from projeto.dao import DestaqueDAO
from projeto.factorys import DestaqueFactory

class DestaqueController:

    def __init__(self):
        self.__dao = DestaqueDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def listar_destaques(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        lista = self.__dao.carregar_destaques()
        destaques = []

        for obj in lista:
            destaques.append(obj.to_dict())

        return jsonify(destaques), 200

    def preparar_gerenciar_destaques(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        return render_template('destaque/gerenciar_destaques.html')

    def cadastrar_destaque(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

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

    def remover_destaque(self, id_destaque):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        self.__dao.remover_destaque(id_destaque)

        return jsonify({'mensagem': 'Destaque removido com sucesso!', 'classe': 'success'}), 200

    def preparar_editar_destaque(self, id_destaque):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        destaque = self.__dao.buscar_destaque_por_id(id_destaque)

        if not destaque:
            flash('Destaque não encontrado.', 'danger')
            return redirect(url_for('destaques.gerenciar_destaques'))

        return render_template('destaque/editar_destaque.html')

    def buscar_destaque_por_id(self, id):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        destaque = self.__dao.buscar_destaque_por_id(id)

        if not destaque:
            return jsonify({'mensagem': 'Destaque não encontrado.', 'classe': 'danger'}), 400

        return jsonify(destaque.to_dict()), 200

    def atualizar_destaque(self, id_destaque):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

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