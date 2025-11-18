from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Customer

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/")
def create_customer(name: str, email: str, phone: str, db: Session = Depends(get_db)):
    customer = Customer(name=name, email=email, phone=phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/")
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()