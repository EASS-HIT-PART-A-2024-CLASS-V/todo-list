from Priority import Priority
from pydantic import BaseModel, Field
from typing import Optional
import datetime

class Task(BaseModel):
    id: Optional[str] = Field(default="", alias="_id")
    title: str
    description: str
    priority: Priority
    due_date: datetime.date

    class Config:
        json_encoders = {
            datetime.date: lambda v: v.strftime("%Y-%m-%d"),
            Priority: lambda v: v.value
        }
        allow_population_by_field_name = True