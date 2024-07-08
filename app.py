from sqlalchemy.exc import StatementError
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

db = SQLAlchemy()


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    CORS(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/books', methods=['GET'])
    def get_books():
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        books = Book.query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "books": [{
                "id": book.id,
                "title": book.title,
                "author": book.author,
                "published_date": book.published_date.strftime('%Y-%m-%d'),
                "isbn": book.isbn,
                "pages": book.pages
            } for book in books.items],
            "total_pages": books.pages,
            "current_page": books.page
        })

    @app.route('/books/<string:isbn>', methods=['GET'])
    def get_book(isbn):
        book = Book.query.filter_by(isbn=isbn).first_or_404()
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
        except StatementError as e:
            db.session.rollback()
            return jsonify({"error": "Invalid request", "message": "A book with this ISBN already exists."}), 400

    @app.route('/books/<string:isbn>', methods=['PUT'])
    def update_book(isbn):
        try:
            book = Book.query.filter_by(isbn=isbn).first_or_404()
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
        except StatementError as e:
            db.session.rollback()
            return jsonify({"error": "Invalid request", "message": "A book with this ISBN already exists."}), 400

    @app.route('/books/<string:isbn>', methods=['DELETE'])
    def delete_book(isbn):
        try:
            book = Book.query.filter_by(isbn=isbn).first()
            if book:
                db.session.delete(book)
                db.session.commit()
                return jsonify({"message": "Book deleted successfully!"})
            else:
                return jsonify({"message": "Resource not found"}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Internal server error", "message": str(e)}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"message": "An internal error occurred"}), 500

    @app.errorhandler(StatementError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({"message": "A book with this ISBN already exists."}), 400

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
