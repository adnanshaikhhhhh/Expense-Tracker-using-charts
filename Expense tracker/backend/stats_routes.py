from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional, Literal
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Expense
from database import SessionLocal
from stats_models import (
    CategoryStats,
    OverallStats,
    DailyStats,
    WeeklyStats,
    MonthlyStats
)

# Create router for stats endpoints
router = APIRouter(prefix="/api/stats", tags=["Statistics"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/by-category", response_model=List[CategoryStats])
def get_stats_by_category(
    start_date: Optional[date] = Query(None, description="Filter from date"),
    end_date: Optional[date] = Query(None, description="Filter to date"),
    db: Session = Depends(get_db)
):
    """
    Get total spending by category
    
    Returns aggregated spending for each category including:
    - Total amount spent
    - Number of expenses
    - Average expense amount
    """
    try:
        # Build query
        query = db.query(
            Expense.category,
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count'),
            func.avg(Expense.amount).label('average')
        )
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        results = query.group_by(Expense.category).order_by(func.sum(Expense.amount).desc()).all()
        
        # Format response
        stats = []
        for category, total, count, average in results:
            stats.append({
                'category': category,
                'total': round(total, 2),
                'count': count,
                'average': round(average, 2)
            })
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/total", response_model=OverallStats)
def get_stats_total(
    start_date: Optional[date] = Query(None, description="Filter from date"),
    end_date: Optional[date] = Query(None, description="Filter to date"),
    db: Session = Depends(get_db)
):
    """
    Get overall spending statistics
    
    Returns:
    - Total amount spent
    - Number of expenses
    - Average, minimum, and maximum expense amounts
    """
    try:
        # Build query
        query = db.query(
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count'),
            func.avg(Expense.amount).label('average'),
            func.min(Expense.amount).label('min'),
            func.max(Expense.amount).label('max')
        )
        
        if start_date:
            query = query.filter(Expense.date >= start_date)
        
        if end_date:
            query = query.filter(Expense.date <= end_date)
        
        result = query.first()
        
        # Handle case when no expenses exist
        if result[0] is None:
            return {
                'total': 0,
                'count': 0,
                'average': 0,
                'min': 0,
                'max': 0
            }
        
        return {
            'total': round(result[0], 2),
            'count': result[1],
            'average': round(result[2], 2),
            'min': round(result[3], 2),
            'max': round(result[4], 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-date")
def get_stats_by_date(
    start_date: Optional[date] = Query(None, description="Filter from date"),
    end_date: Optional[date] = Query(None, description="Filter to date"),
    grouping: Literal["daily", "weekly"] = Query("daily", description="Grouping type"),
    db: Session = Depends(get_db)
):
    """
    Get spending by date (daily or weekly breakdown)
    
    - **grouping**: Choose 'daily' for day-by-day or 'weekly' for week-by-week
    """
    try:
        # Build query based on grouping
        if grouping == 'daily':
            query = db.query(
                Expense.date,
                func.sum(Expense.amount).label('total'),
                func.count(Expense.id).label('count')
            )
            
            if start_date:
                query = query.filter(Expense.date >= start_date)
            
            if end_date:
                query = query.filter(Expense.date <= end_date)
            
            results = query.group_by(Expense.date).order_by(Expense.date.desc()).all()
            
            # Format response
            stats = []
            for date_val, total, count in results:
                stats.append({
                    'date': str(date_val),
                    'total': round(total, 2),
                    'count': count
                })
        else:  # weekly
            query = db.query(
                func.strftime('%Y-W%W', Expense.date).label('week'),
                func.min(Expense.date).label('start_date'),
                func.max(Expense.date).label('end_date'),
                func.sum(Expense.amount).label('total'),
                func.count(Expense.id).label('count')
            )
            
            if start_date:
                query = query.filter(Expense.date >= start_date)
            
            if end_date:
                query = query.filter(Expense.date <= end_date)
            
            results = query.group_by(func.strftime('%Y-W%W', Expense.date)).order_by(func.strftime('%Y-W%W', Expense.date).desc()).all()
            
            # Format response
            stats = []
            for week, start, end, total, count in results:
                stats.append({
                    'week': week,
                    'start_date': str(start),
                    'end_date': str(end),
                    'total': round(total, 2),
                    'count': count
                })
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-month", response_model=List[MonthlyStats])
def get_stats_by_month(db: Session = Depends(get_db)):
    """
    Get spending by month
    
    Returns monthly aggregated spending with totals, counts, and averages
    """
    try:
        results = db.query(
            func.strftime('%Y-%m', Expense.date).label('month'),
            func.sum(Expense.amount).label('total'),
            func.count(Expense.id).label('count'),
            func.avg(Expense.amount).label('average')
        ).group_by(func.strftime('%Y-%m', Expense.date)).order_by(func.strftime('%Y-%m', Expense.date).desc()).all()
        
        stats = []
        for month, total, count, average in results:
            stats.append({
                'month': month,
                'total': round(total, 2),
                'count': count,
                'average': round(average, 2)
            })
        
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))