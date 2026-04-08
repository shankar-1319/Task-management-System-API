from pydantic import BaseModel

class TaskSchema(BaseModel):
    title:str
    description:str
    status :bool=False

class TaskSchemaWithId(BaseModel):
    id:int
    title:str
    description:str
    status :bool=False

class TaskResponseSchema(BaseModel):
    id:int
    title:str

class AllTaskResponseSchema(BaseModel):
    id:int
    title:str
    description:str
    status :bool