from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Sale, Book

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/")
def create_sale(book_id: int, customer_id: int, quantity: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock or book not found")
    total_price = book.price * quantity
    sale = Sale(book_id=book_id, customer_id=customer_id, quantity=quantity, total_price=total_price)
    book.stock -= quantity
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

@router.get("/")
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()

@router.get("/")
def list_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()