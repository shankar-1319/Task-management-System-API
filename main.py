from fastapi import FastAPI
from src.utils.db import Base, engine
from src.task.models import TaskModel
from src.user.models import UserModel
from src.task.router import task_route
from src.user.router import user_routes
# from fastapi.middleware.cors import CORSMiddleware # For development only

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created ✅")

app=FastAPI(title="My API", description="This is my API", version="1.0.0")
app.include_router(task_route) # connects the task route to main file
app.include_router(user_routes)

# For development only
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],   
#     allow_methods=["*"],
#     allow_headers=["*"],
# )