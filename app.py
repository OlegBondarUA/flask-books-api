from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
# CORS(app)
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


# GET /books: отримати список усіх книг
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


# GET /books/<id>: Отримати деталі певної книги за ідентифікатором
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify({
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "published_date": book.published_date.strftime('%Y-%m-%d'),
        "isbn": book.isbn,
        "pages": book.pages
    })


# POST /books: Додати нову книгу
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(
        title=data['title'],
        author=data['author'],
        published_date=datetime.strptime(data['published_date'], '%Y-%m-%d').date(),
        isbn=data['isbn'],
        pages=data['pages']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!", "id": new_book.id}), 201


# PUT /books/<id>: оновити наявну книгу за ідентифікатором
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.json
    book.title = data['title']
    book.author = data['author']
    book.published_date = datetime.strptime(data['published_date'], '%Y-%m-%d').date()
    book.isbn = data['isbn']
    book.pages = data['pages']
    db.session.commit()
    return jsonify({"message": "Book updated successfully!"})


# DELETE /books/<id>: видалення книги за ідентифікатором
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"})


if __name__ == '__main__':
    app.run(debug=True)
