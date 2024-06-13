from fastapi import FastAPI, HTTPException, Depends, Body, status
from sqlalchemy import Engine, text, create_engine
from Schema import ConfigurationSchema, UpdateConfigurationSchema
from database import  get_engine, SessionLocal
from sqlalchemy.orm import Session
# from Model import CountryConfiguration
from Model import CountryConfiguration, create_tables

app = FastAPI()

# engine = create_engine('postgresql://postgres:Galaxy-M31@localhost:5432/CogoportDB')

def get_db():
    db = SessionLocal()
    
    # with engine.begin() as db:
    #     yield db
    try:
        yield db
    finally:
        db.close()

def check_database_connection(db: Session):  # Remove Depends(get_db)
    try:
        # Execute a simple query (e.g., SELECT 1)
        result = db.execute(text("SELECT 1"))
        result.fetchone()  # Optional: Fetch the result to ensure successful execution
        return True
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False

# Example usage with get_db dependency
# if check_database_connection(get_db()):
#     print("Database connection established successfully!")
# else:
#     print("Error connecting to database!")


@app.get("/test_db")
def test_db(db: Session = Depends(get_db)):
    if check_database_connection(db):
        return {"status": "Database connection established successfully!"}
    else:
        raise HTTPException(status_code=500, detail="Error connecting to database")


# @app.post("/create_configuration/{country_code}")
# async def create_configuration(
#     configuration: ConfigurationSchema, db: Session = Depends(get_db)
# ):
#     # Retrieve or create the Country object based on country_code
#     country = (
#         db.query(Country).filter(Country.code == configuration.country_code).first()
#     )
#     if not country:
#         country = Country(
#             code=configuration.country_code, name="Country Name to be Added Later"
#         )  # Placeholder for country name
#         db.add(country)
#         db.commit()
#         db.refresh(country)  # Refresh object to get assigned ID
#     # Create the Configuration object associated with the Country
#     new_configuration = Configuration(**configuration, country_id=country.id)
#     db.add(new_configuration)
#     db.commit()
#     db.refresh(new_configuration)
#     return Configuration(
#         id=new_configuration.id, country_code=country.code, **configuration.dict()
#     )


@app.post("/create_configuration")
async def create_configuration(config: ConfigurationSchema = Body(...), db: Session = Depends(get_db)):
    # Check for existing configuration for the country
    existing_config = db.query(CountryConfiguration).filter_by(country_code=config.country_code).first()
    if existing_config:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Configuration already exists for this country")

    # Convert Pydantic model to SQLAlchemy model
    new_config = CountryConfiguration(
        country_code=config.country_code,
        configurations=config.configurations
    )

    # Add the new configuration to the database
    db.add(new_config)
    db.commit()
    db.refresh(new_config)

    return {"message": "Configuration created successfully!"}


@app.get("/get_configuration/{country_code}")
async def get_configuration(country_code: str, db: Session = Depends(get_db)):
    # """Retrieves the configuration for a specific country."""
    configuration = (
        db.query(CountryConfiguration)
        .filter(country_code == country_code)
        .first()
    )
    if not configuration:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration for country with code {country_code} not found",
        )
    return {
        "id":configuration.id,
        "country_code":configuration.country_code,
        "configuration":configuration.configurations,
    }


@app.put("/update_configuration/{country_code}")
async def update_configuration(
    country_code: str,
    configuration_update: UpdateConfigurationSchema = Body(...),
    db: Session = Depends(get_db),
):
    # """Updates the configuration for a specific country."""
    configuration = (
        db.query(CountryConfiguration)
        .filter(country_code == country_code)
        .first()
    )
    if not configuration:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration for country with code {country_code} not found",
        )

    # Update specific fields based on the request data
    for field, value in configuration_update.dict(exclude_unset=True).items():
        setattr(configuration, field, value)

    db.add(configuration)
    db.commit()
    db.refresh(configuration)
    return {
        "id": configuration.id,
        "country_code": configuration.country_code,
        "configurations": configuration.configurations,
    }

@app.delete("/delete_configuration/{country_code}")
async def delete_configuration(country_code: str, db: Session = Depends(get_db)):
    """Deletes the configuration for a specific country."""
    configuration = db.query(CountryConfiguration).filter_by(country_code=country_code).first()
    if not configuration:
        raise HTTPException(
            status_code=404,
            detail=f"Configuration for country with code {country_code} not found",
        )

    db.delete(configuration)
    db.commit()
    return {
        "message": f"Configuration for country with code {country_code} deleted successfully"
    }


if __name__ == "__main__":
    create_tables()