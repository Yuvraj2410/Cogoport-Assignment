from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base, engine


def create_tables():
    """Creates all tables defined in the `Base` class using the provided engine.

    This function is typically called once at the application startup to ensure
    database tables are created if they don't already exist.
    """
    Base.metadata.create_all(engine)

class CountryConfiguration(Base):
    """Represents a configuration associated with a specific country.

    This model defines a table named "country_configurations" with the following columns:

    - id (Integer, primary key): Unique identifier for the country configuration.
    - country_code (String, unique, not nullable): The ISO 3166-1 alpha-2 code of the country.
    - configurations (JSON, not nullable): A JSON object containing country-specific configurations.
    """
    __tablename__ = "country_configurations"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, unique=True, index=True, nullable=False)
    configurations = Column(JSON, nullable=False)
