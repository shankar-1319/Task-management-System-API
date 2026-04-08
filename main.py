from fastapi import FastAPI
from src.utils.db import Base, engine
from src.task.models import TaskModel
from src.task.router import task_route
# from fastapi.middleware.cors import CORSMiddleware # For development only

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created ✅")

app=FastAPI(title="My API", description="This is my API", version="1.0.0")
app.include_router(task_route) # connects the task route to main fle

# For development only
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],   
#     allow_methods=["*"],
#     allow_headers=["*"],
# )