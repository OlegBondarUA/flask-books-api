import unittest
from app import create_app, db, Book, TestConfig


class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_get_books_empty(self):
        response = self.client.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['books']), 0)

    def test_get_book_not_found(self):
        response = self.client.get('/books/1234567890')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Resource not found', response.json['message'])

    def test_add_book(self):
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890",
            "pages": 200
        }
        response = self.client.post('/books', json=book_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

        # Check if the book is actually added
        added_book = db.session.query(Book).get(response.json['id'])
        self.assertEqual(added_book.title, book_data['title'])

    def test_add_book_missing_field(self):
        book_data = {
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890",
            "pages": 200
        }
        response = self.client.post('/books', json=book_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request', response.json['error'])
        self.assertIn("Missing required field: 'title'", response.json['message'])

    def test_update_book(self):
        # Add a book first
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890",
            "pages": 200
        }
        add_response = self.client.post('/books', json=book_data)
        self.assertEqual(add_response.status_code, 201)

        # Update the book
        update_data = {
            "title": "Updated Test Book",
            "author": "Updated Test Author",
            "published_date": "2024-01-01",
            "isbn": "1234567890",
            "pages": 250
        }
        update_response = self.client.put(f'/books/{book_data["isbn"]}', json=update_data)
        self.assertEqual(update_response.status_code, 200)
        self.assertIn('Book updated successfully!', update_response.json['message'])

        # Check if the book is actually updated
        updated_book = db.session.query(Book).get(add_response.json['id'])
        self.assertEqual(updated_book.title, update_data['title'])

    def test_update_book_invalid_date_format(self):
        # Add a book first
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890",
            "pages": 200
        }
        add_response = self.client.post('/books', json=book_data)
        self.assertEqual(add_response.status_code, 201)

        # Update the book with invalid date format
        update_data = {
            "title": "Updated Test Book",
            "author": "Updated Test Author",
            "published_date": "2024/01/01",
            "isbn": "1234567890",
            "pages": 250
        }
        update_response = self.client.put(f'/books/{book_data["isbn"]}', json=update_data)
        self.assertEqual(update_response.status_code, 400)
        self.assertIn('Invalid request', update_response.json['error'])
        self.assertIn('time data', update_response.json['message'])

    def test_delete_book(self):
        # Add a book first
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890",
            "pages": 200
        }
        add_response = self.client.post('/books', json=book_data)
        self.assertEqual(add_response.status_code, 201)

        # Delete the book
        delete_response = self.client.delete(f'/books/{book_data["isbn"]}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('Book deleted successfully!', delete_response.json['message'])

        # Check if the book is actually deleted
        deleted_book = db.session.query(Book).get(add_response.json['id'])
        self.assertIsNone(deleted_book)

    def test_add_book_existing_isbn(self):
        # Add a book first
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_date": "2023-01-01",
            "isbn": "1234567890",
            "pages": 200
        }
        add_response = self.client.post('/books', json=book_data)
        self.assertEqual(add_response.status_code, 201)

        # Try to add another book with the same ISBN
        duplicate_book_data = {
            "title": "Duplicate Book",
            "author": "Duplicate Author",
            "published_date": "2023-02-01",
            "isbn": "1234567890",
            "pages": 250
        }
        duplicate_response = self.client.post('/books', json=duplicate_book_data)
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertIn('Invalid request', duplicate_response.json['error'])
        self.assertIn('A book with this ISBN already exists.', duplicate_response.json['message'])

    def test_delete_book_not_found(self):
        response = self.client.delete('/books/invalid_isbn')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Resource not found', response.json['message'])


if __name__ == '__main__':
    unittest.main()
