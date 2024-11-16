from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

import model

from datetime import datetime




from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

itens = Blueprint('itens', __name__, url_prefix='/item')

# Suponha que temos uma lista de dicionários para simular um banco de dados
itens_db = []

# Rota para exibir todas as listas (List)
@itens.route('/')
def list_itens():
    data = model.list_all_itens()
    return render_template('itens/index.html' , data=data)



@itens.route('/cadastrar', methods=['GET', 'POST'])
def create_iten():
    if request.method == 'POST':
        # Receber os dados do formulário
        name = request.form['name']
        description = request.form['description']
        tag = request.form.get('tag')  # 'get' retorna None se o campo não for preenchido
        data_closing = request.form.get('data_closing')  # Pode ser None se o campo não for preenchido
        


        # Criar a nova lista
        data = model.create_list(name,description,tag,data_closing)
        
        
        return redirect(url_for('itens.list_itens'))
    
    return render_template('itens/create_iten.html')

# Rota para editar uma lista (Update)
@itens.route('/editar/<int:id>', methods=['GET', 'POST'])
def update_list(id):
    list_item = next((l for l in itens_db if l['id'] == id), None)
    if not list_item:
        return f"Lista com id {id} não encontrada", 404
    
    if request.method == 'POST':
        list_item['name'] = request.form['name']
        flash('Lista atualizada com sucesso!', 'success')
        return redirect(url_for('itens.list_itens'))
    
    return render_template('itens/update_list.html', list_item=list_item)

# Rota para deletar uma lista (Delete)
@itens.route('/deletar/<int:id>', methods=['POST'])
def delete_list(id):
    global itens_db
    itens_db = [l for l in itens_db if l['id'] != id]
    flash('Lista deletada com sucesso!', 'success')
    return redirect(url_for('itens.list_itens'))




# Rota para visualizar os detalhes de uma lista (View)
@itens.route('ver/<int:list_id>')
def view_list(list_id):
    list_item = next((l for l in itens_db if l['list_id'] == id), None)
    if not list_item:
        return f"Lista com id {id} não encontrada", 404
    return render_template('itens/view_list.html', list_item=list_item)

# Função para configurar o blueprint
def configure(app):
    app.register_blueprint(itens)






