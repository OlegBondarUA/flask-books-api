# flask-books-api

1. Clone the repository:
    ```bash
    git clone https://github.com/OlegBondarUA/flask-books-api.git
    cd flask-books-api
   
2. Set up a virtual environment (optional but recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt

4. Run the application:
    ```bash
    python app.py

5. Populate the database with initial data:
    ```bash
   python populate_db.py

The server will be launched at http://127.0.0.1:5000. On the main page, you can view the list of books, 
edit existing books, add new ones, and delete books.