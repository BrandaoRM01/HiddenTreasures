from flask import flash, render_template, redirect, session, url_for, request
from projeto.dao import EcossistemaDAO
from projeto.factorys import EcossistemaFactory

class EcossistemaController:

    def __init__(self):
        self.__dao = EcossistemaDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def listar_ecossistemas(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return self.preparar_gerenciar_ecossistemas()

    def preparar_gerenciar_ecossistemas(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        lista = self.__dao.carregar_ecossistemas()

        return render_template('gerenciar_ecossistemas.html', lista=lista)

    def cadastrar_ecossistema(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        nome = request.form.get('nome')

        nomes_ecossistemas = self.__dao.pegar_nomes_ecossistemas()

        if not nome:
            flash('O campo nome do ecossistema é obrigatório.', 'danger')
            return redirect(url_for('ecossistemas.gerenciar_ecossistemas'))

        if nome.capitalize().strip() in nomes_ecossistemas:
            flash('Já existe um ecossistema com esse nome. Por favor, escolha outro nome.', 'danger')
            return redirect(url_for('ecossistemas.gerenciar_ecossistemas'))

        novo_ecossistema = EcossistemaFactory.criar_ecossistema(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_ecossistema(novo_ecossistema)

        flash('Ecossistema cadastrado com sucesso!', 'success')
        return redirect(url_for('ecossistemas.gerenciar_ecossistemas'))

    def remover_ecossistema(self, id_ecossistema):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        self.__dao.remover_ecossistema(id_ecossistema)

        flash('Ecossistema removido com sucesso!', 'success')
        return redirect(url_for('ecossistemas.gerenciar_ecossistemas'))

    def preparar_editar_ecossistema(self, id_ecossistema):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        ecossistema = self.__dao.buscar_ecossistema_por_id(id_ecossistema)

        if not ecossistema:
            flash('Ecossistema não encontrado.', 'danger')
            return redirect(url_for('ecossistemas.gerenciar_ecossistemas'))

        return render_template('editar_ecossistema.html', ecossistema=ecossistema)

    def atualizar_ecossistema(self, id_ecossistema):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        nome = request.form.get('nome')

        nomes_ecossistemas = self.__dao.pegar_nomes_ecossistemas()

        ecossistema_atual = self.__dao.buscar_ecossistema_por_id(id_ecossistema)

        if not nome:
            flash('O campo nome do ecossistema é obrigatório.', 'danger')
            return redirect(url_for('ecossistemas.atualizar_ecossistema', id=id_ecossistema))

        if nome.capitalize().strip() in nomes_ecossistemas and nome.capitalize().strip() != ecossistema_atual.nome:
            flash('Já existe um ecossistema com esse nome.', 'danger')
            return redirect(url_for('ecossistemas.atualizar_ecossistema', id=id_ecossistema))

        ecossistema_atualizado = EcossistemaFactory.criar_ecossistema(
            nome=nome.capitalize().strip(),
            id=id_ecossistema
        )

        self.__dao.atualizar_ecossistema(ecossistema_atualizado)

        flash('Ecossistema atualizado com sucesso!', 'success')
        return redirect(url_for('ecossistemas.gerenciar_ecossistemas'))