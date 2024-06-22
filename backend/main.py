from fastapi import FastAPI, HTTPException
from Task import Task

app = FastAPI()
todos_local_storage = []
tasks_id_counter = 0

@app.get("/todo/getfullist", description="return all current tasks")
def get_full_todo_list():
    return todos_local_storage 


@app.get("/todo/searchtasks", description="return a single task based on the task title")
def search_tasks(title: str):
    tasks_to_return = []
    try:
        for task in todos_local_storage:
            if title.lower() in task.title.lower():
                tasks_to_return.append(task)
        return tasks_to_return
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/todo/addtask", description="add a single task to the TODO list")
def add_task(task: Task):
    global tasks_id_counter
    try:
        task.id = tasks_id_counter
        todos_local_storage.append(task)
        tasks_id_counter += 1
        return task
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/todo/updatesingletask", description="update a single task based on the task id")
def update_todo(updated_task: Task):
    for task in todos_local_storage:
        if task.id == updated_task.id:
            try:
                task.title = updated_task.title if updated_task.title is not None else task.title
                task.description = updated_task.description if updated_task.description is not None else task.description
                task.priority = updated_task.priority if updated_task.priority is not None else task.priority
                task.due_date = updated_task.due_date if updated_task.due_date is not None else task.due_date
                return task
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
    
    raise HTTPException(status_code=400, detail=f"No such task with id: {updated_task.id}")


@app.delete("/todo/deletesingletask", description="delete a single tasl from the list based on the task id")
def remove_single_task(id: int):
    for task in todos_local_storage:
        if task.id == id:
            try:
                todos_local_storage.remove(task)
                return (f"task {id} removed successfuly")
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
        
    raise HTTPException(status_code=400, detail=f"No such task with id: {id}")


@app.delete("/todo/deletefulllist", description="delete all current tasks on the list")
def remove_all_list():
    try:
        todos_local_storage.clear()
        return (f"task list removed successfuly")
    except Exception as e:
        raise HTTPException(status_code=200, detail=str(e))