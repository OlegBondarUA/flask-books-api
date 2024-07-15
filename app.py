from sqlalchemy.exc import StatementError
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from models import db, Book
from http import HTTPStatus


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
        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "books": [book.to_dict() for book in pagination.items],
            "total_pages": pagination.pages,
            "current_page": pagination.page
        })

    @app.route('/books/<string:isbn>', methods=['GET'])
    def get_book(isbn):
        return jsonify(Book.query.filter_by(isbn=isbn).first_or_404().to_dict())

    @app.route('/books', methods=['POST'])
    def add_book():
        try:
            new_book = Book(**request.json)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({"message": "Book added successfully!", "id": new_book.id}), HTTPStatus.CREATED
        except (KeyError, ValueError) as e:
            return jsonify({"error": "Invalid request", "message": str(e)}), HTTPStatus.BAD_REQUEST
        except StatementError:
            db.session.rollback()
            return jsonify({"error": "Invalid request", "message": "A book with this ISBN already exists."}), HTTPStatus.BAD_REQUEST

    @app.route('/books/<string:isbn>', methods=['PUT'])
    def update_book(isbn):
        try:
            book = Book.query.filter_by(isbn=isbn).first_or_404()
            book.update(request.json)
            db.session.commit()
            return jsonify({"message": "Book updated successfully!"})
        except (KeyError, ValueError) as e:
            return jsonify({"error": "Invalid request", "message": str(e)}), HTTPStatus.BAD_REQUEST
        except StatementError:
            db.session.rollback()
            return jsonify({"error": "Invalid request", "message": "A book with this ISBN already exists."}), HTTPStatus.BAD_REQUEST

    @app.route('/books/<string:isbn>', methods=['DELETE'])
    def delete_book(isbn):
        book = Book.query.filter_by(isbn=isbn).first()
        if not book:
            return jsonify({"message": "Resource not found"}), HTTPStatus.NOT_FOUND
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully!"})

    @app.errorhandler(HTTPStatus.BAD_REQUEST)
    def bad_request(error):
        return jsonify({"error": "Bad request", "message": str(error)}), HTTPStatus.BAD_REQUEST

    @app.errorhandler(HTTPStatus.NOT_FOUND)
    def not_found(error):
        return jsonify({"message": "Resource not found"}), HTTPStatus.NOT_FOUND

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
    def internal_error(error):
        return jsonify({"message": "An internal error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR

    @app.errorhandler(StatementError)
    def handle_integrity_error(error):
        db.session.rollback()
        return jsonify({"message": "A book with this ISBN already exists."}), HTTPStatus.BAD_REQUEST

    return app


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///books.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


if __name__ == '__main__':
    app = create_app(Config)
    app.run(debug=True)