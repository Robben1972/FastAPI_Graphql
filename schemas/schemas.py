from pydantic import BaseModel

class BookInput(BaseModel):
    title: str
    author: str
    year: int


class Book(BaseModel): 
    id: int
    title: str
    author: str
    year: int