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
				const isbn = isbnInput.value;
				const bookId = bookIdInput.value;
				const bookData = {
						title: titleInput.value,
						author: authorInput.value,
						published_date: publishedDateInput.value,
						isbn: isbn,
						pages: pagesInput.value
				};

				if (isbn && bookId) {
						updateBook(isbn, bookData);
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
                            <button class="edit" data-isbn="${book.isbn}">Edit</button>
                            <button class="delete" data-isbn="${book.isbn}">Delete</button>
                        </div>
                    `;
                    bookList.appendChild(li);
                });

                updatePaginationUI(totalPages, currentPage);

                document.querySelectorAll('.edit').forEach(button => {
                    button.addEventListener('click', function() {
                        const isbn = this.dataset.isbn;
                        fetch(`/books/${isbn}`)
                            .then(response => response.json())
                            .then(book => {
                                populateForm(book);
                            });
                    });
                });

                document.querySelectorAll('.delete').forEach(button => {
                    button.addEventListener('click', function() {
                        const isbn = this.dataset.isbn;
                        deleteBook(isbn);
                    });
                });
            });
    }

    function populateForm(book) {
        bookIdInput.value = book.id;
        titleInput.value = book.title;
        authorInput.value = book.author;
        publishedDateInput.value = book.published_date;
        isbnInput.value = book.isbn;
        pagesInput.value = book.pages;
        formTitle.innerText = 'Edit Book';
        cancelEditButton.style.display = 'inline';
    }

    function resetForm() {
        bookIdInput.value = '';
        titleInput.value = '';
        authorInput.value = '';
        publishedDateInput.value = '';
        isbnInput.value = '';
        pagesInput.value = '';
        formTitle.innerText = 'Add Book';
        cancelEditButton.style.display = 'none';
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
                return response.json().then(error => {
                    throw new Error(error.message);
                });
            }
            errorMessage.style.display = 'none';
            resetForm();
            fetchBooks();
        })
        .catch(error => {
            errorMessage.innerText = error.message;
            errorMessage.style.display = 'block';
        });
    }

    function updateBook(isbn, bookData) {
        fetch(`/books/${isbn}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(bookData),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.message);
                });
            }
            errorMessage.style.display = 'none';
            resetForm();
            fetchBooks();
        })
        .catch(error => {
            errorMessage.innerText = error.message;
            errorMessage.style.display = 'block';
        });
    }

    function deleteBook(isbn) {
        fetch(`/books/${isbn}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(error => {
                    throw new Error(error.message);
                });
            }
            errorMessage.style.display = 'none';
            fetchBooks();
        })
        .catch(error => {
            errorMessage.innerText = error.message;
            errorMessage.style.display = 'block';
        });
    }

    function updatePaginationUI(totalPages, currentPage) {
        paginationContainer.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.innerText = i;
            button.addEventListener('click', function() {
                fetchBooks(i);
            });
            if (i === currentPage) {
                button.classList.add('active');
            }
            paginationContainer.appendChild(button);
        }
    }

    fetchBooks();
});
