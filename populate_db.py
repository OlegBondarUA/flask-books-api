from app import db, Book, create_tables, app
from datetime import datetime


create_tables()

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
    }
]

with app.app_context():
    for book_data in books:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            published_date=datetime.strptime(book_data['published_date'], '%Y-%m-%d').date(),
            isbn=book_data['isbn'],
            pages=book_data['pages']
        )
        db.session.add(book)

    db.session.commit()
    print("Books have been added to the database.")
