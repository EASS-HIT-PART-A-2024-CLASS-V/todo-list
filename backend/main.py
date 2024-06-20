from typing import Optional
from fastapi import FastAPI, HTTPException
from datetime import date
from Task import Task
from Priority import Priority

app = FastAPI()
todos_local_storage = []
tasks_id_counter = 0

@app.get("/todo/getfullist", description="return all current tasks")
def get_full_todo_list():
    return todos_local_storage 


@app.get("/todo/getsingletask", description="return a single task based on the task id")
def get_single_task(id: int):
    for task in todos_local_storage:
        if task.id == id:
            return task
        
    raise HTTPException(status_code=400, detail=f"No such task with id: {id}")


@app.post("/todo/addtask", description="add a single task to the TODO list")
def add_task(title: str, description: str, priority: Priority, due_date: date):
    global tasks_id_counter
    try:
        task = Task(id=tasks_id_counter, title=title, description=description, priority=priority, due_date=due_date)
        todos_local_storage.append(task)
        tasks_id_counter += 1
        return task
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.put("/todo/updatesingletask", description="update a single task based on the task id")
def update_todo(id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[Priority] = None, due_date: Optional[date] = None):
    for task in todos_local_storage:
        if task.id == id:
            task.title = title if title is not None else task.title
            task.description = description if description is not None else task.description
            task.priority = priority if priority is not None else task.priority
            task.due_date = due_date if due_date is not None else task.due_date
            return task
    
    raise HTTPException(status_code=400, detail=f"No such task with id: {id}")


@app.delete("/todo/deletesingletask", description="delete a single tasl from the list based on the task id")
def remove_single_task(id: int):
    for task in todos_local_storage:
        if task.id == id:
            todos_local_storage.remove(task)
            raise HTTPException(status_code=200, detail=f"task {id} removed successfuly")
        
    raise HTTPException(status_code=400, detail=f"No such task with id: {id}")


@app.delete("/todo/deletefulllist", description="delete all current tasks on the list")
def remove_all_list():
    try:
        todos_local_storage.clear()
        raise HTTPException(status_code=200, detail=f"task list removed successfuly")
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))