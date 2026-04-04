from flask import render_template, request, redirect, url_for, flash, session
from projeto.dao import AvaliacaoDAO, PontoTuristicoDAO, UserDAO
from projeto.models import Avaliacao
from datetime import datetime

class AvaliacaoController:

    def __init__(self):
        self.__dao_avaliacao = AvaliacaoDAO()
        self.__dao_ponto = PontoTuristicoDAO()
        self.__dao_user = UserDAO()

    def preparar_detalhes_ponto(self, id):
        ponto = self.__dao_ponto.buscar_ponto_por_id(id)

        if not ponto:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.pontos_turisticos'))

        return redirect(url_for('pontos.detalhes_ponto', id=id))
    
    def preparar_editar_avaliacao(self, ponto_id):
        if 'usuario' not in session:
            return render_template('erro.html')

        usuario_email = session['usuario']['email']
        avaliacao = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)

        if not avaliacao:
            flash('Avaliação não encontrada.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))

        ponto = self.__dao_ponto.buscar_ponto_por_id(ponto_id)

        if not ponto:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))

        return render_template('editar_avaliacao.html', avaliacao=avaliacao, ponto=ponto)
    
    def preparar_avaliacoes_ponto(self, ponto_id):
        ponto = self.__dao_ponto.buscar_ponto_por_id(ponto_id)
        usuario_email = None
        avaliacao_usuario = None

        if not ponto:
            flash('Ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.pontos_turisticos'))

        if 'usuario' in session:
            usuario_email = session['usuario']['email']
            avaliacao_usuario = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)
    
        avaliacoes = self.__dao_avaliacao.listar_avaliacoes_por_ponto(ponto_id, usuario_email)

        return render_template('avaliacoes_ponto.html', avaliacoes=avaliacoes, ponto=ponto, avaliacao_usuario=avaliacao_usuario)

    def cadastrar_avaliacao(self, ponto_id):
        if 'usuario' not in session:
            return render_template('erro.html')

        usuario_email = session['usuario']['email']
        nota = request.form.get('nota')
        comentario = request.form.get('comentario')
        data_avaliacao = datetime.now()

        usuario = self.__dao_user.buscar_usuario_por_email(usuario_email)
        ponto = self.__dao_ponto.buscar_ponto_por_id(ponto_id)

        if not usuario or not ponto:
            flash('Usuário ou ponto turístico não encontrado.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))

        avaliacao_existente = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)

        if avaliacao_existente:
            flash('Você já avaliou este ponto turístico. Edite a avaliação existente ou remova-a antes de criar uma nova.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))
        
        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                flash('A nota deve ser um número inteiro entre 1 e 5.', 'danger')
                return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))
        except ValueError:
            flash('A nota deve ser um número inteiro entre 1 e 5.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))
        
        if not nota:
            flash('A nota é obrigatória para cadastrar uma avaliação.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))
        
        if comentario:
            comentario = comentario.strip().capitalize()
        
        nova_avaliacao = Avaliacao(
            usuario=usuario,
            ponto_turistico=ponto,
            nota=nota,
            comentario=comentario,
            data_avaliacao=data_avaliacao
        )

        self.__dao_avaliacao.cadastrar_avaliacao(nova_avaliacao)
        flash('Avaliação cadastrada com sucesso!', 'success')

        return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))
    
    def remover_avaliacao(self, usuario_email, ponto_id):
        if 'usuario' not in session:
            return render_template('erro.html')

        usuario_email_atual = session['usuario']['email']
        tipo_usuario = session['usuario']['tipo_usuario']

        if usuario_email != usuario_email_atual and tipo_usuario not in ['admin', 'superadmin']:
            flash('Você só pode remover sua própria avaliação.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))

        avaliacao = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)
        if not avaliacao:
            flash('Avaliação não encontrada.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))

        self.__dao_avaliacao.remover_avaliacao(usuario_email, ponto_id)
        flash('Avaliação removida com sucesso!', 'success')
        return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))
    
    def atualizar_avaliacao(self, ponto_id):
        if 'usuario' not in session:
            return render_template('erro.html')

        usuario_email = session['usuario']['email']
        nota = request.form.get('nota')
        comentario = request.form.get('comentario')

        avaliacao = self.__dao_avaliacao.buscar_avaliacao(usuario_email, ponto_id)

        if not avaliacao:
            flash('Avaliação não encontrada.', 'danger')
            return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))

        try:
            nota = int(nota)
            if nota < 1 or nota > 5:
                flash('A nota deve ser um número inteiro entre 1 e 5.', 'danger')
                return redirect(url_for('avaliacoes.editar_avaliacao', ponto_id=ponto_id))
        except ValueError:
            flash('A nota deve ser um número inteiro entre 1 e 5.', 'danger')
            return redirect(url_for('avaliacoes.editar_avaliacao', ponto_id=ponto_id))
        
        if not nota:
            flash('A nota é obrigatória para atualizar a avaliação.', 'danger')
            return redirect(url_for('avaliacoes.editar_avaliacao', ponto_id=ponto_id))
        
        if comentario:
            comentario = comentario.strip().capitalize()

        avaliacao_atualizada = Avaliacao(
            usuario=avaliacao.usuario,
            ponto_turistico=avaliacao.ponto_turistico,
            nota=nota,
            comentario=comentario,
            data_avaliacao=avaliacao.data_avaliacao
        )

        self.__dao_avaliacao.atualizar_avaliacao(avaliacao_atualizada)
        flash('Avaliação atualizada com sucesso!', 'success')

        return redirect(url_for('pontos.detalhes_ponto', id=ponto_id))