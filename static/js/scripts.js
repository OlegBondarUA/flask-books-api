document.addEventListener('DOMContentLoaded', function() {
  const bookList = document.getElementById('books');
  const form = document.getElementById('form');
  const inputs = ['book-id', 'title', 'author', 'published_date', 'isbn', 'pages'].reduce((acc, id) => ({ ...acc, [id]: document.getElementById(id) }), {});
  const formTitle = document.getElementById('form-title');
  const cancelEditButton = document.getElementById('cancel-edit');
  const paginationContainer = document.getElementById('pagination');
  const errorMessage = document.getElementById('error-message');

  form.addEventListener('submit', handleFormSubmit);
  cancelEditButton.addEventListener('click', resetForm);

  function handleFormSubmit(event) {
    event.preventDefault();
    const formData = Object.keys(inputs).reduce((acc, key) => ({ ...acc, [key]: inputs[key].value }), {});
    const { 'book-id': bookId, ...bookData } = formData;

    if (bookId && bookData.isbn) {
      updateBook(bookData.isbn, bookData);
    } else {
      addBook(bookData);
    }
  }

  function fetchBooks(page = 1, perPage = 5) {
    fetch(`/books?page=${page}&per_page=${perPage}`)
      .then(response => response.json())
      .then(({ books, total_pages, current_page }) => {
        renderBooks(books);
        updatePaginationUI(total_pages, current_page);
      })
      .catch(handleError);
  }

  function renderBooks(books) {
    bookList.innerHTML = books.map(book => `
      <li>
        ${book.title} by ${book.author}
        <div>
          <button class="edit" data-isbn="${book.isbn}">Edit</button>
          <button class="delete" data-isbn="${book.isbn}">Delete</button>
        </div>
      </li>
    `).join('');

    bookList.querySelectorAll('.edit').forEach(button => button.addEventListener('click', () => editBook(button.dataset.isbn)));
    bookList.querySelectorAll('.delete').forEach(button => button.addEventListener('click', () => deleteBook(button.dataset.isbn)));
  }

  function editBook(isbn) {
    fetch(`/books/${isbn}`)
      .then(response => response.json())
      .then(book => {
        populateForm(book);
      })
      .catch(handleError);
  }

  function populateForm(book) {
    Object.keys(inputs).forEach(key => {
      if (key === 'book-id') {
        inputs[key].value = book.id;
      } else {
        inputs[key].value = book[key] || '';
      }
    });
    formTitle.innerText = 'Edit Book';
    cancelEditButton.style.display = 'inline';
  }

  function resetForm() {
    Object.values(inputs).forEach(input => input.value = '');
    formTitle.innerText = 'Add Book';
    cancelEditButton.style.display = 'none';
  }

  function addBook(bookData) {
    sendRequest('/books', 'POST', bookData);
  }

  function updateBook(isbn, bookData) {
    sendRequest(`/books/${isbn}`, 'PUT', bookData);
  }

  function deleteBook(isbn) {
    sendRequest(`/books/${isbn}`, 'DELETE');
  }

  function sendRequest(url, method, data = null) {
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    fetch(url, options)
      .then(response => {
        if (!response.ok) {
          return response.json().then(error => { throw new Error(error.message); });
        }
        errorMessage.style.display = 'none';
        resetForm();
        fetchBooks();
      })
      .catch(handleError);
  }

  function handleError(error) {
    errorMessage.innerText = error.message;
    errorMessage.style.display = 'block';
  }

  function updatePaginationUI(totalPages, currentPage) {
    paginationContainer.innerHTML = Array.from({ length: totalPages }, (_, i) => i + 1)
      .map(i => `<button ${i === currentPage ? 'class="active"' : ''}>${i}</button>`)
      .join('');

    paginationContainer.querySelectorAll('button').forEach(button =>
      button.addEventListener('click', () => fetchBooks(parseInt(button.innerText)))
    );
  }

  fetchBooks();
});