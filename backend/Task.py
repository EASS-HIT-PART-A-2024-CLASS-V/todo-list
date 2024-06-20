from Priority import Priority
from pydantic import BaseModel
from datetime import date

class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: Priority
    due_date: date