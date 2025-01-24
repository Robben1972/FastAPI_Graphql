# FastAPI with GraphQL Example

This repository demonstrates how to connect **FastAPI** with **GraphQL**, implementing basic queries and mutations for a simple book management system.

## Features

### Queries
1. **getBooks**: Retrieve a list of all books.
2. **getBook**: Retrieve a single book by its `id`.

### Mutations
1. **createBook**: Add a new book to the database.
2. **updateBook**: Update an existing book's details by `id`.
3. **deleteBook**: Remove a book by `id`.

### Book Schema
Each book includes the following fields:
- **id**: Unique identifier for the book (auto-generated).
- **title**: Title of the book (string).
- **author**: Author of the book (string).
- **year**: Year the book was published (integer).

---

## Getting Started

### Prerequisites
- Python 3.9 or higher installed on your system.
- PostgreSQL installed and running.
- Dependencies listed in `requirements.txt`.

### Installation
1. Clone this repository:
    ```bash
    git clone git@github.com:Robben1972/FastAPI_Graphql.git
    cd FastAPI_Graphql
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate       # On Linux/Mac
    venv\Scripts\activate          # On Windows
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `.env` file with your PostgreSQL connection details:
    Create a `.env` file in the root directory with the following content:
    ```env
    DB_URL=postgresql://<username>:<password>@<host>:<port>/<database_name>
    ```

    Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your PostgreSQL credentials.

5. Initialize the database:
    ```bash
    python runner.py
    ```

---

## Usage

To run the application, execute the following command:
```bash
python runner.py
```

The server will start, and you can access the GraphQL Playground at:  
`http://127.0.0.1:8000/graphql`

---

## Folder Structure
```
.
├── actions/
│   ├── mutations.py           # Mutation resolvers
│   ├── queries.py             # Query resolvers
├── schemas/
│   ├── schemas.py             # Pydantic models
│   ├── strawberry_schemas.py  # GraphQL schema definitions
├── config.py                  # Configuration settings
├── database.py                # Database connection logic
├── main.py                    # FastAPI app initialization
├── models.py                  # SQLAlchemy models
├── runner.py                  # Entry point to run the FastAPI server
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables for DB connection
└── .gitignore                 # Ignored files for Git
```

---

## Example Queries and Mutations

### Queries
#### Get All Books
```graphql
query {
  getBooks {
    id
    title
    author
    year
  }
}
```

#### Get a Book by ID
```graphql
query {
  getBook(id: 1) {
    id
    title
    author
    year
  }
}
```

### Mutations
#### Create a Book
```graphql
mutation {
  createBook(title: "1984", author: "George Orwell", year: 1949) {
    id
    title
    author
    year
  }
}
```

#### Update a Book by ID
```graphql
mutation {
  updateBook(id: 1, title: "Animal Farm", author: "George Orwell", year: 1945) {
    id
    title
    author
    year
  }
}
```

#### Delete a Book by ID
```graphql
mutation {
  deleteBook(id: 1) {
    id
    title
    author
    year
  }
}
```

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing
Feel free to fork this repository and submit pull requests for any improvements or additional features!
