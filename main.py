from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from routes.user_routes import router as user_router
from routes.transaction_routes import router as transaction_router
from routes.budget_routes import router as budget_router

from database import engine, Base, db_session


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router, prefix="/api")
app.include_router(transaction_router, prefix="/api")
app.include_router(budget_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "API de Orçamento Mensal!"}

