from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from . import app


db = SQLAlchemy(app)

class Author(db.Model):
    """Data model for Author."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    editable_fields = ['name']

    def __repr__(self):
        return "<Author {}>".format(self.name)
    
    @property
    def get_editable_fields(self):
        return ['name']
    
    @property
    def serialize(self):
        return {
            "id": self.id, 
            "name": self.name
        }


class Book(db.Model):
    """Data model for Book."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('books', lazy=True))
    year_published = db.Column(db.Integer)
    params = db.Column(JSON)

    def __repr__(self):
        return "<Book {}>".format(self.title)

    @property
    def get_editable_fields(self):
        return ['title', 'author_id', 'author', 'year_published', 'params']
    
    @property
    def serialize(self):
        return {
            "id": self.id, 
            "title": self.title,
            "author":self.author.serialize,
            "year_published":self.year_published, 
            "params":self.params
        }