from fastapi import FastAPI
from app.routers import users, auth
from app.db.models.users import create_tables  # import the table creation func

app = FastAPI(
    title="User Order Management API",
    version="1.0.0",
)

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.on_event("startup")
def on_startup():
    create_tables()  # create tables if not exist
    print("✅ Database tables are ready.")

@app.on_event("shutdown")
def on_shutdown():
    print("🛑 App shutting down.")
