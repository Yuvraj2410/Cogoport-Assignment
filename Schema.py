from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy import Column, Integer, String, JSON
from database import Base


class ConfigurationSchema(BaseModel):
    country_code: str
    # india: dict = {'business_name': str, 'pan': str, 'gstin': str}
    
    configurations: Dict[str, Any]

class UpdateConfigurationSchema(BaseModel):
    # country_code: str
    configurations: Dict[str, Any]

