from flask import render_template, flash, redirect, request, session, jsonify
from projeto.dao import PromocaoDAO
from projeto.factorys import PromocaoFactory
from datetime import datetime

class PromocaoController:

    def __init__(self):
        self.__dao = PromocaoDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def preparar_gerenciar_promocoes(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        self.__dao.deletar_promocoes_expiradas()
        
        return render_template('promocao/gerenciar_promocoes.html')
    
    def preparar_editar_promocao(self, id):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        return render_template('promocao/editar_promocao.html')

    def buscar_promocao_por_id(self, id):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403  
            
        promocao = self.__dao.pegar_promocao_por_id(id)
        
        if not promocao:
            return jsonify({'mensagem': 'promocao não encontrada.', 'classe': 'danger'}), 400
        
        return jsonify(promocao.to_dict()), 200

    def listar_promocoes(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 400
        lista = self.__dao.listar_todas_promocoes()
        promocoes = []

        for obj in lista:
            promocoes.append(obj.to_dict())

        return jsonify(promocoes), 200
    
    def cadastrar_promocao(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 400

        dados = request.get_json()
        titulo = dados.get('titulo')
        descricao = dados.get('descricao')
        desconto = dados.get('desconto')
        data_inicio = dados.get('data_inicio')
        data_fim = dados.get('data_fim')

        if not titulo or not desconto or not data_inicio or not data_fim:
            return jsonify({'mensagem': 'Por favor, preencha todos os campos obrigatórios.', 'classe': 'danger'}), 400
        
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'mensagem': 'Formato de data inválido.', 'classe': 'danger'}), 400
        
        try:
            desconto = float(desconto)
            if desconto <= 0 or desconto > 100:
                return jsonify({'mensagem': 'Desconto deve ser entre 1 e 100.', 'classe': 'danger'}), 400
        except ValueError:
            return jsonify({'mensagem': 'Desconto inválido.', 'classe': 'danger'}), 400
        
        if descricao:
            descricao = descricao.capitalize().strip()

        if self.__dao.buscar_promocao_por_titulo(titulo):
            return jsonify({'mensagem': 'Já existe uma promoção com este título.', 'classe': 'danger'}), 400
        
        if data_inicio >= data_fim:
            return jsonify({'mensagem': 'A data de início deve ser anterior à data de fim.', 'classe': 'danger'}), 400
        
        if data_fim < datetime.now().date():
            return jsonify({'mensagem': 'A data de fim deve ser no futuro.', 'classe': 'danger'}), 400
        
        nova_promocao = PromocaoFactory.criar_promocao(
            titulo=titulo.capitalize().strip(),
            descricao=descricao,
            desconto=desconto,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        self.__dao.cadastrar_promocao(nova_promocao)
        return jsonify({'mensagem': 'Promoção cadastrada com sucesso!', 'classe': 'success'}), 200
    
    def remover_promocao(self, id):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 400
        
        promocao = self.__dao.pegar_promocao_por_id(id)
        if not promocao:
            return jsonify({'mensagem': 'Promoção não encontrada.', 'classe': 'danger'}), 400
        
        self.__dao.deletar_promocao(id)
        return jsonify({'mensagem': 'Promoção removida com sucesso!', 'classe': 'success'}), 200
    
    def editar_promocao(self, id):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 400
        
        promocao_atualizada = self.__dao.pegar_promocao_por_id(id)
        if not promocao_atualizada:
            return jsonify({'mensagem': 'Promoção não encontrada.', 'classe': 'danger'}), 400

        dados = request.get_json()
        titulo = dados.get('titulo')
        descricao = dados.get('descricao')
        desconto = dados.get('desconto')
        data_inicio = dados.get('data_inicio')
        data_fim = dados.get('data_fim')

        if not titulo or not desconto or not data_inicio or not data_fim:
            return jsonify({'mensagem': 'Por favor, preencha todos os campos obrigatórios.', 'classe': 'danger'}), 400
        
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'mensagem': 'Formato de data inválido.', 'classe': 'danger'}), 400
        
        try:
            desconto = float(desconto)
            if desconto <= 0 or desconto > 100:
                return jsonify({'mensagem': 'Desconto deve ser entre 1 e 100.', 'classe': 'danger'}), 400
        except ValueError:
            return jsonify({'mensagem': 'Desconto inválido.', 'classe': 'danger'}), 400
        
        if descricao:
            descricao = descricao.capitalize().strip()

        promocao_existente = self.__dao.buscar_promocao_por_titulo(titulo)
        if promocao_existente and promocao_existente.id != id:
            return jsonify({'mensagem': 'Já existe uma promoção com este título.', 'classe': 'danger'}), 400
        
        if data_inicio >= data_fim:
            return jsonify({'mensagem': 'A data de início deve ser anterior à data de fim.', 'classe': 'danger'}), 400
        
        if data_fim < datetime.now().date():
            return jsonify({'mensagem': 'A data de fim deve ser no futuro.', 'classe': 'danger'}), 400
        
        promocao_atualizada = PromocaoFactory.criar_promocao(
            id=id,
            titulo=titulo.capitalize().strip(),
            descricao=descricao,
            desconto=desconto,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        self.__dao.atualizar_promocao(promocao_atualizada)
        return jsonify({'mensagem': 'Promoção atualizada com sucesso!', 'classe': 'success'}), 200