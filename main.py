from fastapi import FastAPI
from app.routers import users

app = FastAPI(
    title="User Order Management API",
    version="1.0.0",
)

app.include_router(users.router, prefix="/users", tags=["Users"])

@app.lifespan("startup")
async def on_startup():
    print("✅ App started and DB initialized.")

@app.lifespan("shutdown")
async def on_shutdown():
    print("🛑 App shutting down.")
