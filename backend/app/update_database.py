from app.database import engine
from app.models import Base

# Update the database schema
Base.metadata.create_all(bind=engine)
print("Database updated successfully!")