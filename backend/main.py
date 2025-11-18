from fastapi import FastAPI
from routes import books, customers, sales, auth
from backend.database import Base, engine

# from fastapi import FastAPI
# from routes.auth import router as auth_router
#
# app = FastAPI()
# app.include_router(auth_router)
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bookstore Management API")

# Include routers
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(customers.router)
app.include_router(sales.router)

@app.get("/")
def root():
    return {"message": "Welcome to Bookstore API"}