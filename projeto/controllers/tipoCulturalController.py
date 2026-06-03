from flask import flash, render_template, redirect, session, url_for, request
from projeto.dao import TipoCulturalDAO
from projeto.factorys import TipoCulturalFactory

class TipoCulturalController:

    def __init__(self):
        self.__dao = TipoCulturalDAO()

    def __usuario_pode_moderar(self):
        return 'usuario' in session and session['usuario']['pode_moderar']

    def listar_tipos_culturais(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        return self.preparar_gerenciar_tipos()

    def preparar_gerenciar_tipos(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        lista = self.__dao.carregar_tipos_culturais()

        return render_template('gerenciar_tipos_culturais.html', lista=lista)

    def cadastrar_tipo_cultural(self):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        nome = request.form.get('nome')

        nomes_tipos = self.__dao.pegar_nomes_tipos_culturais()

        if not nome:
            flash('O campo nome do tipo cultural é obrigatório.', 'danger')
            return redirect(url_for('tipos_culturais.gerenciar_tipos_culturais'))

        if nome.capitalize().strip() in nomes_tipos:
            flash('Já existe um tipo cultural com esse nome.', 'danger')
            return redirect(url_for('tipos_culturais.gerenciar_tipos_culturais'))

        novo_tipo = TipoCulturalFactory.criar_tipo_cultural(
            nome=nome.capitalize().strip()
        )

        self.__dao.cadastrar_tipo_cultural(novo_tipo)

        flash('Tipo cultural cadastrado com sucesso!', 'success')
        return redirect(url_for('tipos_culturais.gerenciar_tipos_culturais'))

    def remover_tipo_cultural(self, id_tipo):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        self.__dao.remover_tipo_cultural(id_tipo)

        flash('Tipo cultural removido com sucesso!', 'success')
        return redirect(url_for('tipos_culturais.gerenciar_tipos_culturais'))

    def preparar_editar_tipo(self, id_tipo):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        tipo = self.__dao.buscar_tipo_por_id(id_tipo)

        if not tipo:
            flash('Tipo cultural não encontrado.', 'danger')
            return redirect(url_for('tipos_culturais.gerenciar_tipos_culturais'))

        return render_template('editar_tipo_cultural.html', tipo=tipo)

    def atualizar_tipo_cultural(self, id_tipo):
        if not self.__usuario_pode_moderar():
            return render_template('erro.html')

        nome = request.form.get('nome')

        nomes_tipos = self.__dao.pegar_nomes_tipos_culturais()

        tipo_atual = self.__dao.buscar_tipo_por_id(id_tipo)

        if not nome:
            flash('O campo nome do tipo cultural é obrigatório.', 'danger')
            return redirect(url_for('tipos_culturais.atualizar_tipo_cultural', id=id_tipo))

        if nome.capitalize().strip() in nomes_tipos and nome.capitalize().strip() != tipo_atual.nome:
            flash('Já existe um tipo cultural com esse nome.', 'danger')
            return redirect(url_for('tipos_culturais.atualizar_tipo_cultural', id=id_tipo))

        tipo_atualizado = TipoCulturalFactory.criar_tipo_cultural(
            nome=nome.capitalize().strip(),
            id=id_tipo
        )

        self.__dao.atualizar_tipo_cultural(tipo_atualizado)

        flash('Tipo cultural atualizado com sucesso!', 'success')
        return redirect(url_for('tipos_culturais.gerenciar_tipos_culturais'))