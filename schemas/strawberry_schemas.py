import strawberry

@strawberry.type
class BookType:
    id: int
    title: str
    author: str
    year: int