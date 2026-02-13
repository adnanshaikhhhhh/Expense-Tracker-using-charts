from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal, Base
from stats_routes import router as stats_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracker API")

# Include stats router
app.include_router(stats_router)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root
@app.get("/")
def home():
    return {"message": "Expense Tracker API running"}

# Add expense
@app.post("/expenses", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    return crud.create_expense(db, expense)

# Get all expenses
@app.get("/expenses")
def get_all_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)

# Delete expense
@app.delete("/expenses/{expense_id}")
def remove_expense(expense_id: int, db: Session = Depends(get_db)):
    return crud.delete_expense(db, expense_id)

# Category summary for Pie chart
@app.get("/summary/category")
def category_summary(db: Session = Depends(get_db)):
    data = crud.get_category_summary(db)
    return [{"category": c, "total": t} for c, t in data]

# Monthly summary for Bar chart
@app.get("/summary/monthly")
def monthly_summary(db: Session = Depends(get_db)):
    data = crud.get_monthly_summary(db)
    return [{"month": m, "total": t} for m, t in data]
