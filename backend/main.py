from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from Task import Task
from Priority import Priority
import datetime
import httpx
import os

app = FastAPI()
API_DB_BASE_URL = os.getenv('DB_URL', 'http://localhost:8081')

@app.get("/todo/getfullist", description="return all current tasks")
def get_full_todo_list():
    try:
        with httpx.Client() as client:
            response = client.get(f"{API_DB_BASE_URL}/db/todo/gettaskslist")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve tasks: {e}")


@app.get("/todo/searchtasks", description="return a single task based on the task title")
def search_tasks(title: str):
    try:
        if title:
            with httpx.Client() as client:
                response = client.get(f"{API_DB_BASE_URL}/db/todo/gettasksbytitle?title={title}")
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(status_code=404, detail=f"Task with title {title} not found")
        else:
            raise HTTPException(status_code=400, detail="Task title is required and cannot be empty")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve tasks: {e}")


@app.post("/todo/addtask", description="add a single task to the TODO list")
def add_task(task: Task):
    try:
        if task.title and isinstance(task.priority, Priority) and task.due_date:
            with httpx.Client() as client:
                headers = {"Content-Type": "application/json"}
                task_data = jsonable_encoder(task)
                response = client.post(f"{API_DB_BASE_URL}/db/todo/addtask", headers=headers, json=task_data)
                return response.json()
        else:
            raise HTTPException(status_code=400, detail="Invalid task details")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add task: {e}")


@app.put("/todo/updatesingletask", description="update a single task based on the task id")
def update_todo(updated_task: Task):
    try:
        if updated_task.title and isinstance(updated_task.priority, Priority) and updated_task.due_date and updated_task.id:
            with httpx.Client() as client:
                headers = {"Content-Type": "application/json"}
                task_data = jsonable_encoder(updated_task)
                response = client.put(f"{API_DB_BASE_URL}/db/todo/updatetask", headers=headers, json=task_data)
                return response.json()
        else:
            raise HTTPException(status_code=400, detail="Invalid task details")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update task: {e}")


@app.delete("/todo/deletesingletask", description="delete a single tasl from the list based on the task id")
def remove_single_task(id: str):
    try:
        if id:
            with httpx.Client() as client:
                response = client.delete(f"{API_DB_BASE_URL}/db/todo/deletesingletask?task_id={id}")
                return response.json()
        else:
            raise HTTPException(status_code=400, detail="Task id is required and cannot be empty")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete task: {e}")


@app.delete("/todo/deletefulllist", description="delete all current tasks on the list")
def remove_all_list():
    try:
        with httpx.Client() as client:
            response = client.delete(f"{API_DB_BASE_URL}/db/todo/deletetasklist")
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete tasks: {e}")