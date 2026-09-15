from flask import render_template, request, jsonify
from projeto.dao import CategoriaDAO
from projeto.factorys import CategoriaFactory
from projeto.decoradores import admin_required

class CategoriaController:

    def __init__(self):
        self.__dao = CategoriaDAO()

    def listar_categorias(self):
        lista = self.__dao.carregar_categorias()
        categorias = []

        for obj in lista:
            categorias.append(obj.to_dict())

        return jsonify(categorias), 200

    def preparar_gerenciar_categorias(self):
        return render_template('categoria/gerenciar_categorias.html')

    @admin_required
    def cadastrar_categoria(self, usuario):
        dados = request.get_json()
        nome = dados.get('nome')
        descricao = dados.get('descricao')

        nomes_categorias = self.__dao.pegar_nomes_categorias()

        if not nome:
            return jsonify({'mensagem': 'O campo nome da categoria é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_categorias:
            return jsonify({'mensagem': 'Já existe uma categoria com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 409

        if not descricao:
            descricao = "Sem descrição"

        nova_categoria = CategoriaFactory.criar_categoria(
            nome=nome.capitalize().strip(),
            descricao=descricao.capitalize().strip()
        )

        self.__dao.cadastrar_categoria(nova_categoria)

        return jsonify({'mensagem': 'Categoria cadastrada com sucesso!', 'classe': 'success'}), 201

    @admin_required
    def remover_categoria(self, usuario, id_categoria):
        self.__dao.remover_categoria(id_categoria)

        return jsonify({'mensagem': 'Categoria removida com sucesso!', 'classe': 'success'}), 204

    def preparar_editar_categoria(self, id_categoria):
        return render_template('categoria/editar_categoria.html')

    @admin_required
    def buscar_categoria_por_id(self, usuario, id_categoria):
        categoria = self.__dao.buscar_categoria_por_id(id_categoria)

        if not categoria:
            return jsonify({'mensagem': 'Categoria não encontrada.', 'classe': 'danger'}), 404

        return jsonify(categoria), 200

    @admin_required
    def atualizar_categoria(self, usuario, id_categoria):
        dados = request.get_json()
        nome = dados.get('nome')
        descricao = dados.get('descricao')

        nomes_categorias = self.__dao.pegar_nomes_categorias()

        categoria_atual = self.__dao.buscar_categoria_por_id(id_categoria)

        if not nome:
            return jsonify({'mensagem': 'O campo nome da categoria é obrigatório.', 'classe': 'danger'}), 400

        if nome.capitalize().strip() in nomes_categorias and nome.capitalize().strip() != categoria_atual['nome']:
            return jsonify({'mensagem': 'Já existe uma categoria com esse nome. Por favor, escolha outro nome.', 'classe': 'danger'}), 409

        if not descricao:
            descricao = "Sem descrição"

        categoria_atualizada = CategoriaFactory.criar_categoria(
            nome=nome.capitalize().strip(),
            descricao=descricao.capitalize().strip(),
            id=id_categoria
        )

        self.__dao.atualizar_categoria(categoria_atualizada)
        return jsonify({'mensagem': 'Categoria atualizada com sucesso!', 'classe': 'success'}), 200