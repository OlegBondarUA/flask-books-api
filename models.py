from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    pages = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, published_date, isbn, pages):
        self.title = title
        self.author = author
        self.published_date = datetime.strptime(published_date, '%Y-%m-%d').date()
        self.isbn = isbn
        self.pages = pages

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "published_date": self.published_date.strftime('%Y-%m-%d'),
            "isbn": self.isbn,
            "pages": self.pages
        }

    def update(self, data):
        for key, value in data.items():
            if key == 'published_date':
                setattr(self, key, datetime.strptime(value, '%Y-%m-%d').date())
            else:
                setattr(self, key, value)

    def __repr__(self):
        return f'<Book {self.title} by {self.author}>'