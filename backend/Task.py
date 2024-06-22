from Priority import Priority
from pydantic import BaseModel
from datetime import date
from typing import Optional

class Task(BaseModel):
    id: Optional[int] = 0
    title: str
    description: str
    priority: Priority
    due_date: date