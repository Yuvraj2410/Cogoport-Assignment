from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base, engine


def create_tables():
    Base.metadata.create_all(engine)

# Base.metadata.create_all(engine)

# class Country(Base):
#     __tablename__ = "countries"

#     id = Column(Integer, primary_key=True, index=True)
#     code = Column(String(2), unique=True, nullable=False)
#     name = Column(String, nullable=False)

#     configurations = relationship("Configuration", backref="country")


class CountryConfiguration(Base):
    __tablename__ = "country_configurations"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, unique=True, index=True, nullable=False)
    configurations = Column(JSON, nullable=False)

    # country = relationship("Country")
