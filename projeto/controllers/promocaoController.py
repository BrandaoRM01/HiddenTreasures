from flask import flash, render_template, redirect, url_for, request, session
from projeto.dao import PromocaoDAO
from projeto.models import Promocao
from datetime import datetime

class PromocaoController:

    def __init__(self):
        self.__dao = PromocaoDAO()

    def preparar_gerenciar_promocoes(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        self.__dao.deletar_promocoes_expiradas()
        
        lista_promocoes = self.__dao.listar_todas_promocoes()
        return render_template('gerenciar_promocoes.html', lista_promocoes=lista_promocoes)
    
    def preparar_editar_promocao(self, id):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        promocao = self.__dao.pegar_promocao_por_id(id)
        if not promocao:
            flash('Promoção não encontrada.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        return render_template('editar_promocao.html', promocao=promocao)
    
    def cadastrar_promocao(self):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        desconto = request.form.get('desconto')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        if not titulo or not desconto or not data_inicio or not data_fim:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        try:
            desconto = float(desconto)
            if desconto <= 0 or desconto > 100:
                flash('Desconto deve ser entre 1 e 100.', 'danger')
                return redirect(url_for('promocoes.gerenciar_promocoes'))
        except ValueError:
            flash('Desconto inválido.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        if descricao:
            descricao = descricao.capitalize().strip()

        if self.__dao.buscar_promocao_por_titulo(titulo):
            flash('Já existe uma promoção com este título.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        if data_inicio >= data_fim:
            flash('A data de início deve ser anterior à data de fim.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        if data_fim < datetime.now().date():
            flash('A data de fim deve ser no futuro.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        nova_promocao = Promocao(
            titulo=titulo.capitalize().strip(),
            descricao=descricao,
            desconto=desconto,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        self.__dao.cadastrar_promocao(nova_promocao)
        flash('Promoção cadastrada com sucesso!', 'success')
        return redirect(url_for('promocoes.gerenciar_promocoes'))
    
    def remover_promocao(self, id):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        promocao = self.__dao.pegar_promocao_por_id(id)
        if not promocao:
            flash('Promoção não encontrada.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        self.__dao.deletar_promocao(id)
        flash('Promoção removida com sucesso!', 'success')
        return redirect(url_for('promocoes.gerenciar_promocoes'))
    
    def editar_promocao(self, id):
        if 'usuario' not in session or session['usuario']['tipo_usuario'] not in ['admin', 'superadmin']:
            return render_template('erro.html')
        
        promocao_atualizada = self.__dao.pegar_promocao_por_id(id)
        if not promocao_atualizada:
            flash('Promoção não encontrada.', 'danger')
            return redirect(url_for('promocoes.gerenciar_promocoes'))
        
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        desconto = request.form.get('desconto')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')

        if not titulo or not desconto or not data_inicio or not data_fim:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('promocoes.editar_promocao', id=id))
        
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            flash('Formato de data inválido.', 'danger')
            return redirect(url_for('promocoes.editar_promocao', id=id))
        
        try:
            desconto = float(desconto)
            if desconto <= 0 or desconto > 100:
                flash('Desconto deve ser entre 1 e 100.', 'danger')
                return redirect(url_for('promocoes.editar_promocao', id=id))
        except ValueError:
            flash('Desconto inválido.', 'danger')
            return redirect(url_for('promocoes.editar_promocao', id=id))
        
        if descricao:
            descricao = descricao.capitalize().strip()

        promocao_existente = self.__dao.buscar_promocao_por_titulo(titulo)
        if promocao_existente and promocao_existente.id != id:
            flash('Já existe uma promoção com este título.', 'danger')
            return redirect(url_for('promocoes.editar_promocao', id=id))
        
        if data_inicio >= data_fim:
            flash('A data de início deve ser anterior à data de fim.', 'danger')
            return redirect(url_for('promocoes.editar_promocao', id=id))
        
        if data_fim < datetime.now().date():
            flash('A data de fim deve ser no futuro.', 'danger')
            return redirect(url_for('promocoes.editar_promocao', id=id))
        
        promocao_atualizada = Promocao(
            id=id,
            titulo=titulo.capitalize().strip(),
            descricao=descricao,
            desconto=desconto,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        self.__dao.atualizar_promocao(promocao_atualizada)
        flash('Promoção atualizada com sucesso!', 'success')
        return redirect(url_for('promocoes.gerenciar_promocoes'))