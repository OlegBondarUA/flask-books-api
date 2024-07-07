from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

db = SQLAlchemy()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app)

    # Registration of routes
    with app.app_context():
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

        @app.route('/books', methods=['POST'])
        def add_book():
            try:
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
            except KeyError as e:
                return jsonify({"error": "Invalid request", "message": f"Missing required field: {str(e)}"}), 400
            except ValueError as e:
                return jsonify({"error": "Invalid request", "message": str(e)}), 400

        @app.route('/books/<int:id>', methods=['PUT'])
        def update_book(id):
            try:
                book = Book.query.get_or_404(id)
                data = request.json
                book.title = data['title']
                book.author = data['author']
                book.published_date = datetime.strptime(data['published_date'], '%Y-%m-%d').date()
                book.isbn = data['isbn']
                book.pages = data['pages']
                db.session.commit()
                return jsonify({"message": "Book updated successfully!"})
            except KeyError as e:
                return jsonify({"error": "Invalid request", "message": f"Missing required field: {str(e)}"}), 400
            except ValueError as e:
                return jsonify({"error": "Invalid request", "message": str(e)}), 400
            except Exception as e:
                return jsonify({"error": "Internal server error", "message": str(e)}), 500

        @app.route('/books/<int:id>', methods=['DELETE'])
        def delete_book(id):
            try:
                book = Book.query.get_or_404(id)
                db.session.delete(book)
                db.session.commit()
                return jsonify({"message": "Book deleted successfully!"})
            except Exception as e:
                return jsonify({"error": "Internal server error", "message": str(e)}), 500

        @app.errorhandler(400)
        def bad_request(error):
            return jsonify({"error": "Bad request", "message": str(error)}), 400

        @app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Not found", "message": str(error)}), 404

        @app.errorhandler(500)
        def internal_server_error(error):
            return jsonify({"error": "Internal server error", "message": str(error)}), 500

    return app


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///books.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    pages = db.Column(db.Integer, nullable=False)


if __name__ == '__main__':
    app = create_app(Config)
    app.run(debug=True)
