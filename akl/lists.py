from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

import model

from datetime import datetime




from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

lists = Blueprint('lists', __name__, url_prefix='/')

# Suponha que temos uma lista de dicionários para simular um banco de dados
lists_db = []

# Rota para exibir todas as listas (List)
@lists.route('/')
def list_lists():
    data = model.list_all_lists()
    return render_template('lists/index.html' , data=data)



@lists.route('/cadastrar', methods=['GET', 'POST'])
def create_list():
    if request.method == 'POST':
        # Receber os dados do formulário
        name = request.form['name']
        description = request.form['description']
        tag = request.form.get('tag')  # 'get' retorna None se o campo não for preenchido
        data_closing = request.form.get('data_closing')  # Pode ser None se o campo não for preenchido
        


        # Criar a nova lista
        data = model.create_list(name,description,tag,data_closing)
        
        
        return redirect(url_for('lists.list_lists'))
    
    return render_template('lists/create_list.html')

# Rota para editar uma lista (Update)
@lists.route('/editar/<int:id>', methods=['GET', 'POST'])
def update_list(id):
    list_item = next((l for l in lists_db if l['id'] == id), None)
    if not list_item:
        return f"Lista com id {id} não encontrada", 404
    
    if request.method == 'POST':
        list_item['name'] = request.form['name']
        flash('Lista atualizada com sucesso!', 'success')
        return redirect(url_for('lists.list_lists'))
    
    return render_template('lists/update_list.html', list_item=list_item)

# Rota para deletar uma lista (Delete)
@lists.route('/deletar/<int:id>', methods=['POST'])
def delete_list(id):
    global lists_db
    lists_db = [l for l in lists_db if l['id'] != id]
    flash('Lista deletada com sucesso!', 'success')
    return redirect(url_for('lists.list_lists'))




# Rota para visualizar os detalhes de uma lista (View)
@lists.route('/ver/<int:list_id>')
def view_list(list_id):

    
    list_item = model.get_iten_listid(list_id)
    
    return render_template('lists/view_list.html', list_item=list_item)
    

# Rota para add item na lista
@lists.route('/add/<int:list_id>')
def add_item_list(list_id):

    lista_item = model.set_iten_to_list(1,1,1)
    
    print(lista_item)
    return redirect(url_for('lists.view_list' , list_id = 1))
    
    



# Função para configurar o blueprint
def configure(app):
    app.register_blueprint(lists)






