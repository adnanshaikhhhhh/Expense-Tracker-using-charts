from sqlalchemy.orm import Session
from models import Expense
from datetime import datetime
from sqlalchemy import func

# Add Expense
def create_expense(db: Session, expense):
    db_expense = Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# Get All Expenses
def get_expenses(db: Session):
    return db.query(Expense).all()

# Delete Expense
def delete_expense(db: Session, expense_id: int):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if expense:
        db.delete(expense)
        db.commit()
    return expense

# Category wise total (Pie chart)
def get_category_summary(db: Session):
    return db.query(
        Expense.category,
        func.sum(Expense.amount).label("total")
    ).group_by(Expense.category).all()

# Monthly summary (Bar chart)
def get_monthly_summary(db: Session):
    return db.query(
        func.strftime("%Y-%m", Expense.date).label("month"),
        func.sum(Expense.amount).label("total")
    ).group_by("month").all()
