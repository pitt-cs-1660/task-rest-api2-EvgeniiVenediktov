from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from cc_simple_server.models import TaskCreate
from cc_simple_server.models import TaskRead
from cc_simple_server.database import init_db
from cc_simple_server.database import DB
from contextlib import asynccontextmanager


db = DB()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Init
    yield
    # Clean up 
    print("Cleaning up...")
    db.close()

app = FastAPI(lifespan=lifespan)

############################################
# Edit the code below this line
############################################


@app.get("/")
async def read_root():
    """
    This is already working!!!! Welcome to the Cloud Computing!
    """
    return {"message": "Welcome to the Cloud Computing!"}


# POST ROUTE data is sent in the body of the request
@app.post("/tasks/", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    """
    Create a new task

    Args:
        task_data (TaskCreate): The task data to be created

    Returns:
        TaskRead: The created task data
    """

    id = db.insert_task(task_data)
    return TaskRead(id=id, title=task_data.title, description=task_data.description, completed=task_data.completed)

    


# GET ROUTE to get all tasks
@app.get("/tasks/", response_model=list[TaskRead])
async def get_tasks():
    """
    Get all tasks in the whole wide database

    Args:
        None

    Returns:
        list[TaskRead]: A list of all tasks in the database
    """
    tasks = db.get_tasks()
    return tasks


# UPDATE ROUTE data is sent in the body of the request and the task_id is in the URL
@app.put("/tasks/{task_id}/", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate):
    """
    Update a task by its ID

    Args:
        task_id (int): The ID of the task to be updated
        task_data (TaskCreate): The task data to be updated

    Returns:
        TaskRead: The updated task data
    """
    # check existence
    exists = db.does_task_exist(task_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Not found")

    updated = db.update_task(task_id, task_data)
    return updated



# DELETE ROUTE task_id is in the URL
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    """
    Delete a task by its ID

    Args:
        task_id (int): The ID of the task to be deleted

    Returns:
        dict: A message indicating that the task was deleted successfully
    """
    # check existence
    exists = db.does_task_exist(task_id)
    if not exists:
        raise HTTPException(status_code=404, detail="Not found")

    deleted = db.delete_task(task_id)
    if deleted:
        return {"message": f"Task {task_id} deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Task was not deleted")
    


@app.get("/tasks/{task_id}/")
async def check_existence(task_id: int):
    """
    Check if a task exists by its ID

    Args:
        task_id (int): The ID of the task to be checked
        
    Returns:
        bool: Boolean variable indicating task's existence
    """

    return db.does_task_exist(task_id)