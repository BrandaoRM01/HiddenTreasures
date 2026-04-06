from flask import Blueprint, request
from projeto.controllers import FavoritoController

favoritos_bp = Blueprint('favoritos', __name__)
controller = FavoritoController()

@favoritos_bp.route('/favoritos/<email>')
def favoritos(email):
    return controller.preparar_favoritos(email)

@favoritos_bp.route('/alterar-favorito', methods=['GET', 'POST'])
def alterar_favorito():
    if request.method == 'POST':
        return controller.alterar_favorito()
    return controller.preparar_pagina_anterior()