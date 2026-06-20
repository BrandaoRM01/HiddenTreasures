from flask import flash, render_template, redirect, session, url_for, request
from projeto.dao import DestaqueDAO
from projeto.factorys import DestaqueFactory

class DestaqueController:

    def __init__(self):
        self.__dao = DestaqueDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def listar_destaques(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return self.preparar_gerenciar_destaques()

    def preparar_gerenciar_destaques(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        lista = self.__dao.carregar_destaques()

        return render_template('destaque/gerenciar_destaques.html', lista=lista)

    def cadastrar_destaque(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        nome = request.form.get('nome')

        nomes_destaques = self.__dao.pegar_nomes_destaques()

        if not nome:
            flash('O campo nome do destaque é obrigatório.', 'danger')
            return redirect(url_for('destaques.gerenciar_destaques'))

        if nome.capitalize().strip() in nomes_destaques:
            flash('Já existe um destaque com esse nome. Por favor, escolha outro nome.', 'danger')
            return redirect(url_for('destaques.gerenciar_destaques'))

        novo_destaque = DestaqueFactory.criar_destaque(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_destaque(novo_destaque)

        flash('Destaque cadastrado com sucesso!', 'success')
        return redirect(url_for('destaques.gerenciar_destaques'))

    def remover_destaque(self, id_destaque):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        self.__dao.remover_destaque(id_destaque)

        flash('Destaque removido com sucesso!', 'success')
        return redirect(url_for('destaques.gerenciar_destaques'))

    def preparar_editar_destaque(self, id_destaque):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        destaque = self.__dao.buscar_destaque_por_id(id_destaque)

        if not destaque:
            flash('Destaque não encontrado.', 'danger')
            return redirect(url_for('destaques.gerenciar_destaques'))

        return render_template('destaque/editar_destaque.html', destaque=destaque)

    def atualizar_destaque(self, id_destaque):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        nome = request.form.get('nome')

        nomes_destaques = self.__dao.pegar_nomes_destaques()

        destaque_atual = self.__dao.buscar_destaque_por_id(id_destaque)

        if not nome:
            flash('O campo nome do destaque é obrigatório.', 'danger')
            return redirect(url_for('destaques.atualizar_destaque', id_destaque=id_destaque)
            )

        if nome.capitalize().strip() in nomes_destaques and nome.capitalize().strip() != destaque_atual.nome:
            flash('Já existe um destaque com esse nome. Por favor, escolha outro nome.', 'danger')
            return redirect(url_for('destaques.atualizar_destaque', id_destaque=id_destaque)
            )

        destaque_atualizado = DestaqueFactory.criar_destaque(
            id=id_destaque,
            nome=nome.capitalize().strip()
        )

        self.__dao.atualizar_destaque(destaque_atualizado)

        flash('Destaque atualizado com sucesso!', 'success')
        return redirect(url_for('destaques.gerenciar_destaques'))