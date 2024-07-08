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
    const paginationContainer = document.getElementById('pagination');
    const errorMessage = document.getElementById('error-message');

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

    function fetchBooks(page = 1, perPage = 5) {
        fetch(`/books?page=${page}&per_page=${perPage}`)
            .then(response => response.json())
            .then(data => {
                const books = data.books;
                const totalPages = data.total_pages;
                const currentPage = data.current_page;

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

                updatePaginationUI(totalPages, currentPage);

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

    function addBook(bookData) {
        fetch('/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookData),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message); });
            }
            return response.json();
        })
        .then(data => {
            fetchBooks();
            resetForm();
            errorMessage.style.display = 'none';
        })
        .catch(error => {
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
        });
    }

    function updateBook(bookId, bookData) {
        fetch(`/books/${bookId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookData),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => { throw new Error(data.message); });
            }
            return response.json();
        })
        .then(data => {
            fetchBooks();
            resetForm();
            errorMessage.style.display = 'none';
        })
        .catch(error => {
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
        });
    }

    function deleteBook(bookId) {
        if (confirm('Are you sure you want to delete this book?')) {
            fetch(`/books/${bookId}`, {
                method: 'DELETE',
            })
            .then(response => response.json())
            .then(data => {
                fetchBooks();
            });
        }
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
        errorMessage.style.display = 'none';
    }

    function updatePaginationUI(totalPages, currentPage) {
        paginationContainer.innerHTML = '';

        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.addEventListener('click', function() {
                fetchBooks(i);
            });
            paginationContainer.appendChild(button);
        }
    }

    fetchBooks();
});
