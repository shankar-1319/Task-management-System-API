from fastapi import APIRouter ,Depends,status
from src.task import controller
from src.task.dtos import AllTaskResponseSchema, TaskSchema,TaskSchemaWithId,TaskResponseSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session

task_route = APIRouter(prefix="/tasks")

@task_route.post("/create_new",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED)
def create_new_task(task_data:TaskSchema,db:Session=Depends(get_db)):
    return controller.create_task(task_data,db)


@task_route.get("/all_tasks",response_model=list[AllTaskResponseSchema],status_code=status.HTTP_200_OK)
def get_all_tasks(db:Session=Depends(get_db)):
    return controller.get_all_tasks(db)


@task_route.get("/one_tasks/{task_id}",response_model=TaskResponseSchema,status_code=status.HTTP_200_OK)
def get_one_tasks(task_id:int , db:Session=Depends(get_db)):
    return controller.get_one_tasks(task_id,db)


@task_route.put("/update_task",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED)
def update_task(task_data:TaskSchemaWithId,db:Session=Depends(get_db)):
    return controller.update_task(task_data, db)


@task_route.delete("/delete_task/{task_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id:int,db:Session=Depends(get_db)):
    return controller.delete_task(task_id,db)