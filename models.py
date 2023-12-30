from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'person'  # имя таблицы
    id = db.Column(db.Integer, primary_key=True) # имя колонки = специальный тип (тип данных, первичный ключ)
    gender = db.Column(db.Text)
    age = db.Column(db.Integer)
    education = db.Column(db.Text)

class Answers(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    upper = db.Column(db.Text)
    lower = db.Column(db.Text)
    whatisbefore = db.Column(db.Text)
    whatisafter = db.Column(db.Text)