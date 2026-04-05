from flask import flash, render_template, redirect, session, url_for, request
from projeto.dao import CategoriaDAO
from projeto.models import Categoria

class CategoriaController:

    def __init__(self):
        self.__dao = CategoriaDAO()

    def listar_categorias(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        return self.preparar_gerenciar_categorias()
    
    def preparar_gerenciar_categorias(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        lista = self.__dao.carregar_categorias()

        return render_template('gerenciar_categorias.html', lista=lista)
    
    def cadastrar_categoria(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        nomes_categorias = self.__dao.pegar_nomes_categorias()

        if not nome:
            flash('O campo nome da categoria é obrigatório.', 'danger')
            return redirect(url_for('categorias.gerenciar_categorias'))

        if nome.capitalize().strip() in nomes_categorias:
            flash('Já existe uma categoria com esse nome. Por favor, escolha outro nome.', 'danger')
            return redirect(url_for('categorias.gerenciar_categorias'))

        if not descricao:
            descricao = "Sem descrição"

        nova_categoria = Categoria(
            nome=nome.capitalize().strip(), 
            descricao=descricao.capitalize().strip()
        )

        self.__dao.cadastrar_categoria(nova_categoria)

        flash('Categoria cadastrada com sucesso', 'success')
        return redirect(url_for('categorias.gerenciar_categorias'))
    
    def remover_categoria(self, id_categoria):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        self.__dao.remover_categoria(id_categoria)
        return redirect(url_for('categorias.gerenciar_categorias'))
    
    def preparar_editar_categoria(self, id_categoria):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')

        categoria = self.__dao.buscar_categoria_por_id(id_categoria)

        if not categoria:
            flash('Categoria não encontrada.', 'danger')
            return redirect(url_for('categorias.gerenciar_categorias'))
        return render_template('editar_categoria.html', categoria=categoria)
    
    def atualizar_categoria(self, id_categoria):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')

        nomes_categorias = self.__dao.pegar_nomes_categorias()

        categoria_atual = self.__dao.buscar_categoria_por_id(id_categoria)

        if not nome:
            flash('O campo nome da categoria é obrigatório.', 'danger')
            return redirect(url_for('categorias.atualizar_categoria', id=id_categoria))
        
        if nome.capitalize().strip() in nomes_categorias and nome.capitalize().strip() != categoria_atual['nome']:
            flash('Já existe uma categoria com esse nome. Por favor, escolha outro nome.', 'danger')
            return redirect(url_for('categorias.atualizar_categoria', id=id_categoria))
        
        if not descricao:
            descricao = "Sem descrição"

        categoria_atualizada = Categoria(
            nome=nome.capitalize().strip(),
            descricao=descricao.capitalize().strip(),
            id=id_categoria
        )

        self.__dao.atualizar_categoria(categoria_atualizada)

        return redirect(url_for('categorias.gerenciar_categorias'))