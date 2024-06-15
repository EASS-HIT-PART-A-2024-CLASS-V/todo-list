from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from enum import Enum

app = FastAPI()
todos_local_storage = []

class priority(Enum):
    LOWEST = "1"
    LOW = "2"
    MEDIUM = "3"
    HIGH = "4"
    HIGHEST = "5"


class Task(BaseModel):
    title: str
    description: str
    priority: priority
    due_date: date


@app.get("/todo/getfullist", description="return all current tasks")
def get_full_todo_list():
    return todos_local_storage 


@app.get("/todo/getsingletask", description="return a single task based on the task title")
def get_single_task(title: str):
    for task in todos_local_storage:
        if task.title == title:
            return task
        
    raise HTTPException(status_code=400, detail=f"No such task titled {title}")


@app.post("/todo/addtask", description="add a single task to the TODO list")
def add_todo(title: str, description: str, priority: priority, due_date: date):
    try:
        task = Task(title=title, description=description, priority=priority, due_date=due_date)
        todos_local_storage.append(task)
        return task
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.put("/todo/update/task", description="update a single task based on the task title")
def update_todo(title: str, priority: priority, due_date: Optional[date] = None):
    for task in todos_local_storage:
        if task.title == title:
            task.priority = priority
            task.due_date = due_date if due_date is not None else task.due_date
            return task
    
    raise HTTPException(status_code=400, detail=f"No such task titled {title}")


@app.delete("/todo/removesingletask", description="remove a single tasl from the list based on the task title")
def remove_single_task(title: str):
    for task in todos_local_storage:
        if task.title == title:
            todos_local_storage.remove(task)
            raise HTTPException(status_code=200, detail=f"task removed successfuly")
        
    raise HTTPException(status_code=400, detail=f"No such task titled {title}")


@app.delete("/todo/removealllist", description="remove all current tasks on the list")
def remove_all_list():
    try:
        todos_local_storage.clear()
        raise HTTPException(status_code=200, detail=f"task list removed successfuly")
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))