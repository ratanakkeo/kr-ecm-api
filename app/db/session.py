from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine with the correct URL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # Set to False in production
)

# Create SessionLocal class with the configured engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()