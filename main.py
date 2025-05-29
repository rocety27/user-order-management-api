from fastapi import FastAPI
from app.routers import users, orders, auth
from dotenv import load_dotenv

load_dotenv()  # Load env variables early

app = FastAPI(
    title="User Order Management API",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
@app.on_event("startup")
def on_startup():
    print("🚀 App starting up...")

@app.on_event("shutdown")
def on_shutdown():
    print("🛑 App shutting down.")
