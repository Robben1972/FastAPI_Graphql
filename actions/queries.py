import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from models import get_db
from schemas.strawberry_schemas import BookType
from models import BookModel

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"

    @strawberry.field
    def get_books(self, info) -> List[BookType]:
        db: Session = next(get_db())  
        books = db.query(BookModel).all()
        return [BookType(id=book.id, title=book.title, author=book.author, year=book.year) for book in books]

    @strawberry.field
    def get_book(self, id: int, info) -> Optional[BookType]:
        db: Session = next(get_db())
        book = db.query(BookModel).filter(BookModel.id == id).first()
        if book:
            return BookType(id=book.id, title=book.title, author=book.author, year=book.year)
        return None
