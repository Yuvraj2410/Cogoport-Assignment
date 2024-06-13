from fastapi import FastAPI, HTTPException, Depends, Body, status
from sqlalchemy import Engine, text, create_engine
from Schema import ConfigurationSchema, UpdateConfigurationSchema
from database import  get_engine, SessionLocal
from sqlalchemy.orm import Session
from Model import CountryConfiguration, create_tables

app = FastAPI()

def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.post("/create_configuration")
async def create_configuration(config: ConfigurationSchema = Body(...), db: Session = Depends(get_db)):
    """
    Creates a new configuration for a specific country.

    This endpoint accepts a `ConfigurationSchema` object in the request body.
    It checks for existing configuration for the country and raises an error if
    one exists. Otherwise, it converts the Pydantic model to a SQLAlchemy model
    and adds it to the database.

    - Raises HTTPException with status code 409 if a configuration already exists.
    - Returns a JSON response with a success message on successful creation.
    """
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
    """
    Retrieves the configuration for a specific country.

    This endpoint retrieves the configuration associated with the provided `country_code`
    from the database. It raises an HTTPException with status code 404 if no
    configuration is found.

    - Raises HTTPException with status code 404 if configuration is not found.
    - Returns a JSON response containing the retrieved configuration details.
    """

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
    """
    Updates the configuration for a specific country.

    This endpoint allows updating specific fields of the configuration based on the
    provided `UpdateConfigurationSchema` data in the request body. It first retrieves
    the existing configuration and raises an HTTPException with status code 404 if not found.
    Then, it iterates over the provided update data and sets the corresponding attributes
    on the existing configuration object. Finally, the updated configuration is saved to the database.

    - Raises HTTPException with status code 404 if configuration is not found.
    - Returns a JSON response containing the updated configuration details.
    """
    
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