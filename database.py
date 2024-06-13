from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
from local_settings import DATABASE_URL

# Define the base class for the ORM models
Base = declarative_base()

def get_engine():
    """
    This function creates a database engine using the provided connection URL retrieved from the 'DATABASE_URL' environment variable.
    """
    engine = create_engine(DATABASE_URL)
    return engine


engine = get_engine()
SessionLocal = sessionmaker(bind=engine)
