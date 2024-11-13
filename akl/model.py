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
    data_create = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)  
    data_closing = db.Column(db.DateTime, nullable=True)  
    
    def __repr__(self):
        return f'<Lista {self.name}>'

