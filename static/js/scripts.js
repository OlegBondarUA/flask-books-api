document.addEventListener('DOMContentLoaded', function() {
    const bookList = document.getElementById('books');
    const form = document.getElementById('form');
    const bookIdInput = document.getElementById('book-id');
    const titleInput = document.getElementById('title');
    const authorInput = document.getElementById('author');
    const publishedDateInput = document.getElementById('published_date');
    const isbnInput = document.getElementById('isbn');
    const pagesInput = document.getElementById('pages');
    const formTitle = document.getElementById('form-title');
    const cancelEditButton = document.getElementById('cancel-edit');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const bookId = bookIdInput.value;
        const bookData = {
            title: titleInput.value,
            author: authorInput.value,
            published_date: publishedDateInput.value,
            isbn: isbnInput.value,
            pages: pagesInput.value
        };

        if (bookId) {
            updateBook(bookId, bookData);
        } else {
            addBook(bookData);
        }
    });

    cancelEditButton.addEventListener('click', function() {
        resetForm();
    });

    function fetchBooks() {
        fetch('/books')
            .then(response => response.json())
            .then(books => {
                bookList.innerHTML = '';
                books.forEach(book => {
                    const li = document.createElement('li');
                    li.innerHTML = `
                        ${book.title} by ${book.author}
                        <div>
                            <button class="edit" data-id="${book.id}">Edit</button>
                            <button class="delete" data-id="${book.id}">Delete</button>
                        </div>
                    `;
                    bookList.appendChild(li);
                });

                document.querySelectorAll('.edit').forEach(button => {
                    button.addEventListener('click', function() {
                        const bookId = this.dataset.id;
                        fetch(`/books/${bookId}`)
                            .then(response => response.json())
                            .then(book => {
                                bookIdInput.value = book.id;
                                titleInput.value = book.title;
                                authorInput.value = book.author;
                                publishedDateInput.value = book.published_date;
                                isbnInput.value = book.isbn;
                                pagesInput.value = book.pages;
                                formTitle.textContent = 'Edit Book';
                                cancelEditButton.style.display = 'inline';
                            });
                    });
                });

                document.querySelectorAll('.delete').forEach(button => {
                    button.addEventListener('click', function() {
                        const bookId = this.dataset.id;
                        deleteBook(bookId);
                    });
                });
            });
    }

    function addBook(book) {
        fetch('/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(book)
        })
        .then(response => {
            if (response.ok) {
                fetchBooks();
                form.reset();
            } else {
                alert('Failed to add book');
            }
        });
    }

    function updateBook(bookId, book) {
        fetch(`/books/${bookId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(book)
        })
        .then(response => {
            if (response.ok) {
                fetchBooks();
                resetForm();
            } else {
                alert('Failed to update book');
            }
        });
    }

    function deleteBook(bookId) {
        fetch(`/books/${bookId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (response.ok) {
                fetchBooks();
            } else {
                alert('Failed to delete book');
            }
        });
    }

    function resetForm() {
        bookIdInput.value = '';
        titleInput.value = '';
        authorInput.value = '';
        publishedDateInput.value = '';
        isbnInput.value = '';
        pagesInput.value = '';
        formTitle.textContent = 'Add Book';
        cancelEditButton.style.display = 'none';
    }

    fetchBooks();
});
