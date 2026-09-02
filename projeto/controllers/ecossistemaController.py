from flask import flash, render_template, redirect, session, url_for, request, jsonify
from projeto.dao import EcossistemaDAO
from projeto.factorys import EcossistemaFactory

class EcossistemaController:

    def __init__(self):
        self.__dao = EcossistemaDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def listar_ecossistemas(self):
        lista = self.__dao.carregar_ecossistemas()
        ecossistemas = []

        for obj in lista:
            ecossistemas.append(obj.to_dict())

        return jsonify(ecossistemas), 200

    def preparar_gerenciar_ecossistemas(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return render_template('ecossistema/gerenciar_ecossistemas.html')

    def cadastrar_ecossistema(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        dados = request.get_json()
        nome = dados.get('nome')

        nomes_ecossistemas = self.__dao.pegar_nomes_ecossistemas()

        if not nome:
            return jsonify({'mensagem': 'O campo nome do ecossistema é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_ecossistemas:
            return jsonify({'mensagem': 'Já existe um ecossistema com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 400

        novo_ecossistema = EcossistemaFactory.criar_ecossistema(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_ecossistema(novo_ecossistema)

        return jsonify({'mensagem': 'Ecossistema cadastrado com sucesso!', 'classe': 'success'}), 200

    def remover_ecossistema(self, id_ecossistema):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403

        self.__dao.remover_ecossistema(id_ecossistema)

        return jsonify({'mensagem': 'Ecossistema removido com sucesso!', 'classe': 'success'}), 200

    def preparar_editar_ecossistema(self, id_ecossistema):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return render_template('ecossistema/editar_ecossistema.html')

    def buscar_ecossistema_por_id(self, id):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403  
         
        ecossistema = self.__dao.buscar_ecossistema_por_id(id)
        
        if not ecossistema:
            return jsonify({'mensagem': 'Ecossistema não encontrado.', 'classe': 'danger'}), 400
        
        return jsonify(ecossistema.to_dict()), 200
         
    def atualizar_ecossistema(self, id_ecossistema):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        
        dados = request.get_json()
        nome = dados.get('nome')

        nomes_ecossistemas = self.__dao.pegar_nomes_ecossistemas()

        ecossistema_atual = self.__dao.buscar_ecossistema_por_id(id_ecossistema)

        if not nome:
            return jsonify({'mensagem': 'O campo nome do ecossistema é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_ecossistemas and nome.capitalize().strip() != ecossistema_atual.nome:
            return jsonify({'mensagem': 'Já existe um ecossistema com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 400

        ecossistema_atualizado = EcossistemaFactory.criar_ecossistema(
            nome=nome.capitalize().strip(),
            id=id_ecossistema
        )

        self.__dao.atualizar_ecossistema(ecossistema_atualizado)

        return jsonify({'mensagem': 'Ecossistema atualizado com sucesso!', 'classe': 'success'}), 200