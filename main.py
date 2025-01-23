# app/main.py

import strawberry
from typing import List, Optional
from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- Database Setup ---

DATABASE_URL = "postgresql://user:password@host:port/database"  # Replace with your PostgreSQL connection string

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # Base class for declarative models


# --- Define SQLAlchemy Model ---

class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)


# Create the table in the database
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Pydantic Models (for input validation and data transfer) ---

class BookInput(BaseModel):
    title: str
    author: str
    year: int


class Book(BaseModel):  # Represents data retrieved from the DB
    id: int
    title: str
    author: str
    year: int


# --- Strawberry GraphQL Types ---

@strawberry.type
class BookType:
    id: int
    title: str
    author: str
    year: int


# --- GraphQL Queries ---

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"

    @strawberry.field
    def get_books(self, info) -> List[BookType]:
        """Fetches all books from the database."""
        db: Session = next(get_db())  # Manually handle dependency
        books = db.query(BookModel).all()
        return [BookType(id=book.id, title=book.title, author=book.author, year=book.year) for book in books]

    @strawberry.field
    def get_book(self, id: int, info) -> Optional[BookType]:
        """Fetches a single book by its ID."""
        db: Session = next(get_db())  # Manually handle dependency
        book = db.query(BookModel).filter(BookModel.id == id).first()
        if book:
            return BookType(id=book.id, title=book.title, author=book.author, year=book.year)
        return None


# --- GraphQL Mutations ---

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_book(self, title: str, author: str, year: int, info) -> BookType:
        """Creates a new book in the database."""
        db: Session = next(get_db())  # Manually handle dependency
        db_book = BookModel(title=title, author=author, year=year)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)  # Refresh to get the generated ID
        return BookType(id=db_book.id, title=db_book.title, author=db_book.author, year=db_book.year)

    @strawberry.mutation
    def update_book(self, id: int, title: str, author: str, year: int, info) -> Optional[BookType]:
        """Updates an existing book in the database."""
        db: Session = next(get_db())  # Manually handle dependency
        db_book = db.query(BookModel).filter(BookModel.id == id).first()
        if not db_book:
            return None  # Book not found

        db_book.title = title
        db_book.author = author
        db_book.year = year
        db.commit()
        db.refresh(db_book)
        return BookType(id=db_book.id, title=db_book.title, author=db_book.author, year=db_book.year)

    @strawberry.mutation
    def delete_book(self, id: int, info) -> bool:
        """Deletes a book from the database."""
        db: Session = next(get_db())  # Manually handle dependency
        db_book = db.query(BookModel).filter(BookModel.id == id).first()
        if not db_book:
            return False  # Book not found

        db.delete(db_book)
        db.commit()
        return True

# --- Strawberry Schema ---

schema = strawberry.Schema(query=Query, mutation=Mutation)

# --- FastAPI Setup ---

graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")