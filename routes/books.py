from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Book

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/")
def create_book(title: str, author: str, category: str, price: float, stock: int, isbn: str, db: Session = Depends(get_db)):
    book = Book(title=title, author=author, category=category, price=price, stock=stock, isbn=isbn)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@router.get("/")
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/category/{category_name}")
def get_books_by_category(category_name: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.category.ilike(f"%{category_name}%")).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found in this category")
    return books

@router.get("/author/{author_name}")
def get_books_by_category(author_name: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.author.ilike(f"%{author_name}%")).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found in this author")
    return books


@router.put("/{book_id}")
def update_book(book_id: int, stock: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.stock = stock
    db.commit()
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}