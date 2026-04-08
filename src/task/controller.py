from src.task.dtos import TaskSchema,TaskSchemaWithId
from sqlalchemy.orm import Session
from src.task.models import TaskModel
from fastapi import HTTPException

# Add data to database postgres
def create_task(task_data:TaskSchema,db:Session):
    data = task_data.model_dump()
    new_task = TaskModel(title=data["title"],
                         description=data["description"],
                         status=data["status"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# Get all the values from postgres
def get_all_tasks(db:Session):
    all_tasks=db.query(TaskModel).all()
    return all_tasks


# Get all the values from postgres
def get_one_tasks(task_id:int,db:Session):
    one_tasks=db.query(TaskModel).get(task_id) # may be "one_task = db.get(TaskModel, task_id)"  get() finds for primary key only

    if not one_tasks:
         raise HTTPException(status_code=404,detail="Task Id is incorrect")
    
    return one_tasks


# Update the values in postgres
def update_task(task_data:TaskSchemaWithId,db:Session):

    data = task_data.model_dump()
    task_id=data.get("id")

    task_to_update=db.query(TaskModel).get(task_id)

    if not task_to_update:
        raise HTTPException(status_code=404,detail="Task Id is incorrect")

    for key, value in data.items():
        if key != "id":
            setattr(task_to_update, key, value)

    db.add(task_to_update)
    db.commit()
    db.refresh(task_to_update)
    return task_to_update


# delete TASK 
def delete_task(task_id:int,db:Session):
    print(task_id)
    task_data = db.query(TaskModel).get(task_id)
    if not task_data:
        raise HTTPException(status_code=404,detail="Task Id is incorrect")
    
    db.delete(task_data)
    db.commit()
    return None
