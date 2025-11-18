from backend.database import Base, engine
from backend.models import Sale, Book, Customer

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")