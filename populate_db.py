from app import db, create_app, Book, Config
from datetime import datetime


def initialize_database():
    app = create_app(Config)
    with app.app_context():
        db.create_all()
        print("Database initialized.")


def clean_database():
    app = create_app(Config)
    with app.app_context():
        db.session.query(Book).delete()
        db.session.commit()
        print("Database cleaned.")


def add_books():
    initialize_database()
    clean_database()
    app = create_app(Config)
    with app.app_context():

        books = [
            {
                "title": "To Kill a Mockingbird",
                "author": "Harper Lee",
                "published_date": "1960-07-11",
                "isbn": "9780061120084",
                "pages": 281
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "published_date": "1949-06-08",
                "isbn": "9780451524935",
                "pages": 328
            },
            {
                "title": "Moby-Dick",
                "author": "Herman Melville",
                "published_date": "1851-10-18",
                "isbn": "9781503280786",
                "pages": 720
            },
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "published_date": "1925-04-10",
                "isbn": "9780743273565",
                "pages": 180
            },
            {
                "title": "Pride and Prejudice",
                "author": "Jane Austen",
                "published_date": "1813-01-28",
                "isbn": "9780141439518",
                "pages": 279
            },
            {
                "title": "The Catcher in the Rye",
                "author": "J.D. Salinger",
                "published_date": "1951-07-16",
                "isbn": "9780316769488",
                "pages": 234
            },
            {
                "title": "Brave New World",
                "author": "Aldous Huxley",
                "published_date": "1932-10-27",
                "isbn": "9780060850524",
                "pages": 288
            },
            {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "published_date": "1937-09-21",
                "isbn": "9780261102217",
                "pages": 310
            },
            {
                "title": "The Lord of the Rings",
                "author": "J.R.R. Tolkien",
                "published_date": "1954-07-29",
                "isbn": "9780618640157",
                "pages": 1178
            },
            {
                "title": "Alice's Adventures in Wonderland",
                "author": "Lewis Carroll",
                "published_date": "1865-11-26",
                "isbn": "9780141439761",
                "pages": 272
            },
            {
                "title": "The Adventures of Sherlock Holmes",
                "author": "Arthur Conan Doyle",
                "published_date": "1892-10-14",
                "isbn": "9781593083794",
                "pages": 307
            },
            {
                "title": "The Odyssey",
                "author": "Homer",
                "published_date": "1869-01-01",
                "isbn": "9780143039952",
                "pages": 384
            },
            {
                "title": "War and Peace",
                "author": "Leo Tolstoy",
                "published_date": "1869-01-01",
                "isbn": "9780199232765",
                "pages": 1225
            },
            {
                "title": "Frankenstein",
                "author": "Mary Shelley",
                "published_date": "1818-01-01",
                "isbn": "9780141439471",
                "pages": 280
            },
            {
                "title": "The Picture of Dorian Gray",
                "author": "Oscar Wilde",
                "published_date": "1890-07-20",
                "isbn": "9780141442464",
                "pages": 250
            }
        ]

        for book_data in books:
            if book_data['published_date']:
                published_date = datetime.strptime(book_data['published_date'], '%Y-%m-%d').date()
            else:
                published_date = None

            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                published_date=published_date,
                isbn=book_data['isbn'],
                pages=book_data['pages']
            )
            db.session.add(book)

        db.session.commit()
        print("Books have been added to the database.")


if __name__ == '__main__':
    add_books()
