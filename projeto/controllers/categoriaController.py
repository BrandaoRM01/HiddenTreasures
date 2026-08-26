from flask import flash, render_template, redirect, session, url_for, request, jsonify
from projeto.dao import CategoriaDAO
from projeto.factorys import CategoriaFactory
from projeto.models import categoria

class CategoriaController:

    def __init__(self):
        self.__dao = CategoriaDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def listar_categorias(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        lista = self.__dao.carregar_categorias()
        categorias = []

        for obj in lista:
            categorias.append(obj.to_dict())
        
        return jsonify(categorias)

    def preparar_gerenciar_categorias(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')
        
        return render_template('categoria/gerenciar_categorias.html')
    
    def cadastrar_categoria(self):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        
        dados = request.get_json()
        nome = dados.get('nome')
        descricao = dados.get('descricao')

        nomes_categorias = self.__dao.pegar_nomes_categorias()

        if not nome:
            return jsonify({'mensagem': 'O campo nome da categoria é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_categorias:
            return jsonify({'mensagem': 'Já existe uma categoria com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 400

        if not descricao:
            descricao = "Sem descrição"

        nova_categoria = CategoriaFactory.criar_categoria(
            nome=nome.capitalize().strip(), 
            descricao=descricao.capitalize().strip()
        )

        self.__dao.cadastrar_categoria(nova_categoria)

        return jsonify({'mensagem': 'Categoria cadastrada com sucesso!', 'classe': 'success'}), 200

    def remover_categoria(self, id_categoria):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        
        self.__dao.remover_categoria(id_categoria)

        return jsonify({'mensagem': 'Categoria removida com sucesso!', 'classe': 'success'}), 200
    
    def preparar_editar_categoria(self, id_categoria):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        categoria = self.__dao.buscar_categoria_por_id(id_categoria)

        if not categoria:
            flash('Categoria não encontrada.', 'danger')
            return redirect(url_for('categorias.gerenciar_categorias'))
        return render_template('categoria/editar_categoria.html', categoria=categoria)

    def buscar_categoria_por_id(self, id_categoria):
        if not self.__usuario_pode_moderar():
            return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        categoria = self.__dao.buscar_categoria_por_id(id_categoria)

        if not categoria:
            return jsonify({'mensagem': 'Categoria não encontrada.', 'classe': 'danger'}), 400

        return jsonify(categoria), 200
    
    def atualizar_categoria(self, id_categoria):
        if not self.__usuario_pode_moderar():
           return jsonify({'mensagem': 'você não tem permissão', 'classe': 'danger'}), 403
        
        dados = request.get_json()
        nome = dados.get('nome')
        descricao = dados.get('descricao')

        nomes_categorias = self.__dao.pegar_nomes_categorias()

        categoria_atual = self.__dao.buscar_categoria_por_id(id_categoria)

        if not nome:
            return jsonify({'mensagem': 'O campo nome da categoria é obrigatório.', 'classe': 'danger'})
        
        if nome.capitalize().strip() in nomes_categorias and nome.capitalize().strip() != categoria_atual['nome']:
            return jsonify({'mensagem': 'Já existe uma categoria com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'})
        
        if not descricao:
            descricao = "Sem descrição"

        categoria_atualizada = CategoriaFactory.criar_categoria(
            nome=nome.capitalize().strip(),
            descricao=descricao.capitalize().strip(),
            id=id_categoria
        )

        self.__dao.atualizar_categoria(categoria_atualizada)
        return jsonify({'mensagem': 'Categoria atualizada com sucesso!', 'classe': 'success'})