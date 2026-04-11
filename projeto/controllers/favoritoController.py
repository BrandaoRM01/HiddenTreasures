from flask import render_template, redirect, url_for, session, flash, request
from projeto.dao import FavoritoDAO, PontoTuristicoDAO, UserDAO
from projeto.models import Favorito, User, PontoTuristico

class FavoritoController:

    def __init__(self):
        self.__dao_favoritos = FavoritoDAO()
        self.__dao_pontos = PontoTuristicoDAO()
        self.__dao_usuario = UserDAO()

    def preparar_pagina_anterior(self):
        return redirect(request.referrer or url_for('pontos.index'))

    def preparar_favoritos(self, usuario_email):
        if 'usuario' not in session:
            return render_template('erro.html')
        
        if usuario_email:
            pontos = self.__dao_pontos.listar_pontos()
            favoritos = self.__dao_favoritos.listar_favoritos_por_usuario(usuario_email)

            ids_favoritos = set()

            for favorito in favoritos:
                ids_favoritos.add(favorito.ponto_turistico.id)
        else:
            ids_favoritos = set()

        for ponto in pontos:
            ponto.favorito = ponto.id in ids_favoritos

        tem_favoritos = False

        for ponto in pontos:
            if ponto.favorito:
                tem_favoritos = True
                break  

        return render_template('favoritos.html', pontos=pontos, tem_favoritos=tem_favoritos)
    
    def alterar_favorito(self):
        if 'usuario' not in session:
            return render_template('erro.html')
        
        usuario_email = session['usuario']['email']
        ponto_id = request.form.get('ponto_id')

        if not ponto_id:
            flash('Ponto turístico não encontrado', 'danger')

        if self.__dao_favoritos.verificar_favorito(usuario_email, ponto_id):
            self.__dao_favoritos.deletar_favorito(usuario_email, ponto_id)

            flash('Ponto turístico desfavoritado com sucesso', 'success')
            return redirect(request.referrer or url_for('pontos.index'))
        
        ponto = self.__dao_pontos.buscar_ponto_por_id(ponto_id)

        usuario = self.__dao_usuario.buscar_usuario_por_email(usuario_email)

        novo_favorito = Favorito(
            user=usuario,
            ponto_turistico=ponto
        )

        self.__dao_favoritos.adicionar_favorito(novo_favorito)

        flash('Ponto turístico favoritado com sucesso!', 'success')
        return redirect(request.referrer or url_for('pontos.index'))