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
    active = db.Column(db.Boolean, default=True, nullable=True) 

    
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
        data_closing=data_closing,
        active=True
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
    listas = Lista.query.filter(Lista.active.isnot(False)).all()
    return listas


def get_list_id(list_id):
    """
    Função para recuperar uma lista pelo seu ID.

    :param list_id: O ID da lista a ser recuperada.
    :return: A Lista correspondente ao ID fornecido ou None se não encontrado.
    """
    # Tenta buscar a lista no banco de dados pelo ID
    
    lista = Lista.query.get(list_id)

    if lista:
        return lista
    else:
        return None 




def update_list_id(list_id , name=None, description=None, tag=None, data_closing=None):
    
    lista = get_list_id(list_id)
    
    if name:
        lista.name = name
    if description:
        lista.description = description
    if tag:
        lista.tag = tag


    # Converter data_closing para date, se necessário
    if isinstance(data_closing, str):
        try:
            # Tenta converter a string para um objeto date
            data_closing = datetime.strptime(data_closing, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Formato de data inválido para 'data_closing'. Use o formato 'YYYY-MM-DD'.")
    
    if data_closing:
        lista.data_closing = data_closing
    
    db.session.commit()
    return lista

def delete_list_id(list_id):


    lista = get_list_id(list_id)
        
    if lista:
        lista.active = False
        db.session.commit()

    return lista






class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(120), nullable=False)  
    measure = db.Column(db.String(120), nullable=False)  
    tag = db.Column(db.String(120)) 
    data_create = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)  
    active = db.Column(db.Boolean, default=True, nullable=True) 

    def __repr__(self):
        return f'<Item {self.name}>'




def list_all_itens():
    """
    Função para listar todas as listas no banco de dados.
    :return: Lista de objetos Lista.
    """
    # Recupera todas as listas ordenadas pelo campo 'data_create' (se quiser ordenar de forma diferente, altere aqui)
    itens = Item.query.filter(Item.active.isnot(False)).all()
    return itens


def create_iten(name, description, measure, tag=None):
    """
    Função para criar um novo item e salvar no banco de dados.

    :param name: Nome do item.
    :param description: Descrição do item.
    :param measure: Unidade de medida do item.
    :param tag: Tag associada ao item (opcional).
    :return: A instância do objeto Item criada.
    """
    # Verifica se o nome do item já existe
    if Item.query.filter_by(name=name).first():
        existe = 0
        num = 0
        while existe == 0:
            num += 1
            # Verifica se já existe um item com o nome modificado (por exemplo, "Nome (1)")
            if Item.query.filter_by(name=f"{name} ({num})").first():
                pass
            else:
                name = f"{name} ({num})"
                existe = 1

    # Garantir que data_create seja um objeto date (sem a hora)
    data_create = datetime.utcnow().date()  # Obtém a data atual sem a hora

    # Criação do novo objeto Item
    novo_item = Item(
        name=name,
        description=description,
        measure=measure,
        tag=tag,
        data_create=data_create  # Data de criação automaticamente gerada
    )

    # Adicionando o novo item à sessão do banco de dados
    db.session.add(novo_item)
    db.session.commit()

    return novo_item


def get_iten_id(iten_id):
    """
    Função para recuperar um item pelo seu ID.

    :param item_id: O ID do item a ser recuperado.
    :return: O item correspondente ao ID fornecido ou None se não encontrado.
    """
    # Tenta buscar o item no banco de dados pelo ID
    iten = Item.query.get(iten_id)

    if iten:
        return iten
    else:
        return None 

def update_iten_id(iten_id , name=None, description=None, measure=None, tag=None):
    item = get_iten_id(iten_id)
    
    if name:
        item.name = name
    if description:
        item.description = description
    if measure:
        item.measure = measure
    if tag:
        item.tag = tag
    db.session.commit()
    return item


def delete_iten_id(iten_id):
    item = get_iten_id(iten_id)
    
    item.active = False
    db.session.commit()
    return item
    """
    #para deletar
    if item:
        db.session.delete(item)
        db.session.commit()
        return item
    """



class ListaItem(db.Model):
    __tablename__ = 'lista_item'  # Nome da tabela intermediária
    
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    quantidade = db.Column(db.Integer, nullable=False)  # Quantidade do item na lista
    lista_id = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)  # Chave estrangeira para Lista
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)  # Chave estrangeira para Item

    # Relacionamento com a tabela Lista
    lista = db.relationship('Lista', backref=db.backref('lista_itens', lazy=True))

    # Relacionamento com a tabela Item
    item = db.relationship('Item', backref=db.backref('lista_itens', lazy=True))

    def __repr__(self):
        return f'<ListaItem Lista {self.lista_id} - Item {self.item_id}, Quantidade {self.quantidade}>'




def get_iten_listid(list_id):
    
    #está listando 1 só, mudar para trazer a lista conforme id da lista
    itens_lista = db.session.query(ListaItem).filter(ListaItem.lista_id == list_id).first()
    
    return [itens_lista.item]


def set_iten_to_list(list_id, iten_id , quantidade):
    lista = Lista.query.get(list_id)
    
    item = Item.query.get(iten_id)

    lista_item = ListaItem()
    lista_item.lista_id = lista.id
    
    lista_item.item_id = item.id
    
    lista_item.quantidade = quantidade
    
    db.session.add(lista_item)
    db.session.commit()
    return lista_item


def get_lista_com_itens(lista_id):
    # Buscar a lista pelo ID
    lista = Lista.query.get(lista_id)
    
    # Verificar se a lista foi encontrada
    
    # Buscar os itens dessa lista, incluindo a quantidade de cada item
    lista_itens = []
    for lista_item in lista.lista_itens:  # Acesso via relacionamento (backref)
        lista_itens.append({
            "item_id": lista_item.item.id,
            "item_name": lista_item.item.name,
            "quantidade": lista_item.quantidade,
            "descricao": lista_item.item.description
        })
    
    # Preparar os dados da lista com seus itens
    dados_lista = {
        "id": lista.id,
        "name": lista.name,
        "description": lista.description,
        "data_create": lista.data_create,
        "data_closing": lista.data_closing,
        "tag": lista.tag,
        "itens": lista_itens  # Lista de itens
    }
    
    return dados_lista
