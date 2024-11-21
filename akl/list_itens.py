from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

import model

from datetime import datetime




from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

list_itens = Blueprint('list_itens', __name__, url_prefix='/lista-itens')


# Rota para exibir todas as listas (List)
@list_itens.route('/')
def index():
    data = model.list_all_lists()
    return render_template('list_itens/index.html' , data=data)



# Rota para visualizar os detalhes de uma lista (View)
@list_itens.route('/adicionar/<int:list_id>')
def add_list(list_id):

    
    #list_item = model.get_iten_listid(list_id)
    
    data = model.list_all_itens()
    
    return render_template('lists/add_list.html', data=data)



# Rota para add item na lista
@list_itens.route('/add/<int:list_id>')
def add_item_list(list_id):

    lista_item = model.set_iten_to_list(1,1,1)
    
    print(lista_item)
    return redirect(url_for('lists.view_list' , list_id = 1))
    



# Função para configurar o blueprint
def configure(app):
    app.register_blueprint(list_itens)






