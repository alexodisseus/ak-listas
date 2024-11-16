from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Instância do SQLAlchemy
db = SQLAlchemy()


# Definindo o modelo Lista
class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)  
    tag = db.Column(db.String(120)) 
    data_create = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)  
    data_closing = db.Column(db.Date, nullable=True)  # Agora é do tipo Date (sem hora)
    
    def __repr__(self):
        return f'<Lista {self.name}>'

def create_list(name, description, tag=None, data_closing=None):
    """
    Função para criar uma nova lista e salvar no banco de dados.

    :param name: Nome da lista.
    :param description: Descrição da lista.
    :param tag: Tag associada à lista (opcional).
    :param data_closing: Data de fechamento da lista (opcional).
    :return: A instância do objeto Lista criada.
    """
    # Verifica se o nome da lista já existe
    if Lista.query.filter_by(name=name).first():
        existe = 0
        num = 0
        while existe ==0:
            num = num+1
            if Lista.query.filter_by(name=name+" ("+str(num)+")").first():
                pass
            else:
                name=name+" ("+str(num)+")"
                existe = 1


        
    # Converter data_closing para date, se necessário
    if isinstance(data_closing, str):
        try:
            # Tenta converter a string para um objeto date
            data_closing = datetime.strptime(data_closing, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Formato de data inválido para 'data_closing'. Use o formato 'YYYY-MM-DD'.")

    # Garantir que data_create seja um objeto date, sem a hora
    data_create = datetime.utcnow().date()  # Usando .date() para obter apenas a data (sem hora)

    # Criação do novo objeto Lista
    nova_lista = Lista(
        name=name,
        description=description,
        tag=tag,
        data_create=data_create,  # Passando a data sem a hora
        data_closing=data_closing
    )

    # Adicionando a nova lista à sessão do banco de dados
    db.session.add(nova_lista)
    db.session.commit()

    return nova_lista



def list_all_lists():
    """
    Função para listar todas as listas no banco de dados.
    :return: Lista de objetos Lista.
    """
    # Recupera todas as listas ordenadas pelo campo 'data_create' (se quiser ordenar de forma diferente, altere aqui)
    listas = Lista.query.all()
    return listas



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)  
    measure = db.Column(db.String(120), nullable=False)  
    tag = db.Column(db.String(120)) 
    data_create = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)  
    
    def __repr__(self):
        return f'<Item {self.name}>'




def list_all_itens():
    """
    Função para listar todas as listas no banco de dados.
    :return: Lista de objetos Lista.
    """
    # Recupera todas as listas ordenadas pelo campo 'data_create' (se quiser ordenar de forma diferente, altere aqui)
    itens = Item.query.all()
    return itens