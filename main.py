# main.py

from fastapi import FastAPI
#from app.config.settings import settings  # assuming you have a settings.py
#from app.db.database import init_db  # DB session maker or init logic
from app.routers import user  # adjust as per your actual router files

app = FastAPI(
    title="User Order Management API",
    version="1.0.0",
    #description="FastAPI with SQLAlchemy, Alembic, and Pydantic."
)

# Routers
app.include_router(user.router, prefix="/users", tags=["Users"])  

# Startup Event
@app.lifespan("startup")
async def on_startup():
    #init_db()
    print("✅ App started and DB initialized.")

# Shutdown Event
@app.lifespan("shutdown")
async def on_shutdown():
    print("🛑 App shutting down.")

