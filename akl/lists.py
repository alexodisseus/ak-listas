from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import model


from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

lists = Blueprint('lists', __name__, url_prefix='/')

# Suponha que temos uma lista de dicionários para simular um banco de dados
lists_db = []

# Rota para exibir todas as listas (List)
@lists.route('/')
def list_lists():

    return render_template('lists/index.html')



# Rota para criar uma nova lista (Create)
@lists.route('/cadastrar', methods=['GET', 'POST'])
def create_list():
    if request.method == 'POST':
        name = request.form['name']
        
        # Validação simples: nome não pode ser vazio ou muito curto
        if not name or len(name) < 3:
            flash('O nome da lista deve ter pelo menos 3 caracteres.', 'error')
            return render_template('lists/create_list.html')
        
        # Criando a nova lista e adicionando ao banco de dados simulado
        new_list = {'id': len(lists_db) + 1, 'name': name}
        lists_db.append(new_list)
        
        # Flash message de sucesso
        flash('Lista cadastrada com sucesso!', 'success')
        
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
@lists.route('/visualizar/<int:id>')
def view_list(id):
    list_item = next((l for l in lists_db if l['id'] == id), None)
    if not list_item:
        return f"Lista com id {id} não encontrada", 404
    return render_template('lists/view_list.html', list_item=list_item)

# Função para configurar o blueprint
def configure(app):
    app.register_blueprint(lists)
