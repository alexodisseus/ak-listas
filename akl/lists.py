from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

import model

from datetime import datetime




from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

lists = Blueprint('lists', __name__, url_prefix='/')

# Suponha que temos uma lista de dicionários para simular um banco de dados


# Rota para exibir todas as listas (List)
@lists.route('/')
def list_lists():
    data = model.list_all_lists()
    return render_template('lists/index.html' , data=data)



@lists.route('listas/cadastrar', methods=['GET', 'POST'])
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

@lists.route('listas/editar/<int:list_id>', methods=['GET', 'POST'])
def update_list(list_id):
    data = model.get_list_id(list_id)

    if request.method == 'POST':
        
        name = request.form['name']
        description = request.form['description']
        tag = request.form['tag']
        data_closing = request.form['data_closing']
        
        data = model.update_list_id(list_id, name , description , tag , data_closing)

        flash('Lista atualizada com sucesso!', 'success')
        return redirect(url_for('lists.view_list' , list_id=list_id))
    
    
    return render_template('lists/update_list.html', data=data)



# Rota para deletar uma lista (Delete)
@lists.route('listas/deletar/<int:list_id>')
def delete_list(list_id):
    
    deleted = model.delete_list_id(list_id)
    flash('Lista deletada com sucesso!', 'success')
    return redirect(url_for('lists.list_lists'))




# Rota para visualizar os detalhes de uma lista (View)
@lists.route('listas/ver/<int:list_id>')
def view_list(list_id):

    
    #list_item = model.get_iten_listid(list_id)
    
    list_item = model.get_lista_com_itens(list_id)
    
    return render_template('lists/view_list.html', list_item=list_item)
    

    



# Função para configurar o blueprint
def configure(app):
    app.register_blueprint(lists)






