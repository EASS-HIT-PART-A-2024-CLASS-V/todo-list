from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from Model import TaskModel
import os

app = FastAPI()

# Database connection settings
MONGO_DETAILS = os.getenv("DB_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGO_DETAILS)
database = client["todo-list"]
task_collection = database["task-list"]


@app.get("/db/todo/gettaskslist", response_description="List all tasks")
def get_tasks_list():
    try:
        tasks = list(task_collection.find())
        for task in tasks:
            task["_id"] = str(task["_id"])
        return tasks
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve tasks: {e}")


@app.get("/db/todo/gettasksbytitle", response_description="Get tasks by title")
def get_tasks_by_title(title: str):
    try:
        tasks = list(task_collection.find({"title": {"$regex": title, "$options": "i"}}))
        if tasks:
            for task in tasks:
                task["_id"] = str(task["_id"])
            return tasks
        else:
            raise HTTPException(status_code=404, detail=f"Task with title {title} not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to retrieve tasks: {e}")


@app.post("/db/todo/addtask", response_description="Add new task to db")
def add_task(task: TaskModel):
    try:
        update_dict = task.dict()
        new_task = task_collection.insert_one(update_dict)
        created_task = task_collection.find_one({"_id": new_task.inserted_id})
        return {"_id": str(created_task['_id'])}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to add task: {e}")


@app.put("/db/todo/updatetask", response_description="Update a task")
def update_task(task: TaskModel):
    oid = ObjectId(task.id)

    # Prepare the update dictionary by excluding the '_id' field
    update_dict = task.dict(exclude={"id"})
    try:
        updated_task = task_collection.find_one_and_update(
            {"_id": oid},
            {"$set": update_dict},
            return_document=True
        )

        if updated_task:
            updated_task["_id"] = str(updated_task["_id"])
            return updated_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update task: {e}")


@app.delete("/db/todo/deletesingletask", response_description="Delete a task")
def delete_task(task_id: str):
    oid = ObjectId(task_id)
    try:
        deleted_task = task_collection.find_one_and_delete({"_id": oid})

        if deleted_task:
            deleted_task["_id"] = str(deleted_task["_id"])
            return deleted_task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete task: {e}")


@app.delete("/db/todo/deletetasklist", response_description="Delete all tasks")
def delete_task_list():
    try:
        deleted_tasks = task_collection.delete_many({})
        return {"message": f"{deleted_tasks.deleted_count} tasks deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete tasks: {e}")