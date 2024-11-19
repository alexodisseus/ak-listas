from flask import Flask
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

import model

from datetime import datetime




from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash

itens = Blueprint('itens', __name__, url_prefix='/item')



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
        measure = request.form['measure']
        tag = request.form['tag']
        


        # Criar a nova lista
        data = model.create_iten(name,description,measure,tag)
        
        
        return redirect(url_for('itens.list_itens'))
    
    return render_template('itens/create_iten.html')


# Rota para editar uma lista (Update)

@itens.route('/editar/<int:iten_id>', methods=['GET', 'POST'])
def edit_iten(iten_id):
    
    list_iten = model.get_iten_id(iten_id)
    
    if not list_iten:
        flash("Item não encontrado!", "error")
        return redirect(url_for('items.view_item', item_id=item_id))
    

    if request.method == 'POST':
        # Obtém os dados do formulário
        name = request.form['name']
        description = request.form['description']
        measure = request.form['measure']
        tag = request.form['tag']
        itens = model.update_iten_id(iten_id , name,description,measure,tag)
        
        if itens:
            flash('Lista atualizada com sucesso!', 'success')
            return redirect(url_for('itens.list_itens'))
    


    print(list_iten.id)



    return render_template('itens/update_iten.html', list_iten=list_iten)

















# Rota para deletar uma lista (Delete)
@itens.route('/deletar/<int:iten_id>')
def delete_iten(iten_id):
    
    iten_delete = model.delete_iten_id(iten_id)

    if iten_delete:
        flash('Lista deletada com sucesso!', 'success')
        return redirect(url_for('itens.list_itens'))
    else:
        return f"ite com id {iten_id} não encontrado", 404



# Rota para visualizar os detalhes de uma lista (View)
@itens.route('ver/<int:iten_id>')
def view_iten(iten_id):
    list_item = model.get_iten_id(iten_id)
    if not list_item:
        return f"Lista com id {id} não encontrada", 404
    return render_template('itens/view_iten.html', iten=list_item)

# Função para configurar o blueprint
def configure(app):
    app.register_blueprint(itens)






