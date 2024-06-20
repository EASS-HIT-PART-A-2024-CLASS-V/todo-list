from Priority import Priority
from pydantic import BaseModel
from datetime import date
from typing import Optional
import uuid

class Task(BaseModel):
    task_id: Optional[int]
    title: str
    description: str
    priority: Priority
    due_date: date

    def __init__(self, title: str, description: str, priority: Priority, due_date: date):
        super().__init__(title=title, description=description, priority=priority, due_date=due_date, task_id=None)
        self.task_id = uuid.uuid4()
        