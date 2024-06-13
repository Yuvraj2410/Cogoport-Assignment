from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, JSON
from database import Base


class ConfigurationSchema(BaseModel):
    """
    Schema representing the configuration for a specific country.

    This schema defines the expected structure for data related to country-specific
    configurations.

    - country_code (str): The ISO 3166-1 alpha-2 code of the country.
    - configurations (Dict[str, Any]): A dictionary containing key-value pairs
      specific to the country configuration. The keys can be any string, and
      the values can be of any type supported by Pydantic.
    """
    country_code: str
    # Note: Commented out the example default value. Defining default values
    # for nested dictionaries is generally discouraged as it can lead to unexpected
    # behavior during data validation. It's recommended to explicitly set
    # configurations within the data.
    # india: dict = {'business_name': str, 'pan': str, 'gstin': str}
    
    configurations: Dict[str, Any]

class UpdateConfigurationSchema(BaseModel):
    """
    Schema representing the data used to update an existing country configuration.

    This schema focuses on the `configurations` field, allowing for partial updates
    to the existing configuration data.

    - configurations (Dict[str, Any]): A dictionary containing key-value pairs
      specifying the changes to be made to the existing configuration. Keys and
      values follow the same format as in the `ConfigurationSchema`.
    """
    configurations: Dict[str, Any]

