from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    pages = db.Column(db.Integer, nullable=False)


def create_tables():
    with app.app_context():
        db.create_all()


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "published_date": book.published_date.strftime('%Y-%m-%d'),
        "isbn": book.isbn,
        "pages": book.pages
    } for book in books])


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
