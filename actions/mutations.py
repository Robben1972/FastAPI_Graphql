import strawberry
from models import get_db, BookModel
from schemas.strawberry_schemas import BookType
from typing import Optional
from sqlalchemy.orm import Session

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_book(self, title: str, author: str, year: int, info) -> BookType:
        db: Session = next(get_db())  
        db_book = BookModel(title=title, author=author, year=year)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)  
        return BookType(id=db_book.id, title=db_book.title, author=db_book.author, year=db_book.year)

    @strawberry.mutation
    def update_book(self, id: int, title: str, author: str, year: int, info) -> Optional[BookType]:
        db: Session = next(get_db()) 
        db_book = db.query(BookModel).filter(BookModel.id == id).first()
        if not db_book:
            return None 

        db_book.title = title
        db_book.author = author
        db_book.year = year
        db.commit()
        db.refresh(db_book)
        return BookType(id=db_book.id, title=db_book.title, author=db_book.author, year=db_book.year)

    @strawberry.mutation
    def delete_book(self, id: int, info) -> bool:
        db: Session = next(get_db())
        db_book = db.query(BookModel).filter(BookModel.id == id).first()
        if not db_book:
            return False

        db.delete(db_book)
        db.commit()
        return True