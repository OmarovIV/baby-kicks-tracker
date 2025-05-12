from datetime import datetime
from settings import get_pregnancy_start_date

def calculate_pregnancy_weeks(record_date_str):
    """Return weeks and days since pregnancy start."""
    start_str = get_pregnancy_start_date()
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        record = datetime.strptime(record_date_str, "%Y-%m-%d")
        delta = record - start
        weeks = delta.days // 7
        days = delta.days % 7
        return f"{weeks} weeks {days} days"
    except:
        return "N/A"
