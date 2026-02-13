from pydantic import BaseModel
from typing import List, Optional

class CategoryStats(BaseModel):
    """Statistics for a single category"""
    category: str
    total: float
    count: int
    average: float

class OverallStats(BaseModel):
    """Overall spending statistics"""
    total: float
    count: int
    average: float
    min: float
    max: float

class DailyStats(BaseModel):
    """Daily spending statistics"""
    date: str
    total: float
    count: int

class WeeklyStats(BaseModel):
    """Weekly spending statistics"""
    week: str
    start_date: str
    end_date: str
    total: float
    count: int

class MonthlyStats(BaseModel):
    """Monthly spending statistics"""
    month: str
    total: float
    count: int
    average: float