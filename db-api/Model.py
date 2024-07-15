from pydantic import BaseModel, Field
from typing import Optional

class TaskModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    description: str
    priority: str
    due_date: str

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "60f1e9c0e6d4b9b7d4f1f5b3",
                "title": "take the dog out",
                "description": "take the dog out for a walk",
                "priority": "HIGH",
                "due_date": "2021-08-01"
            }
        }