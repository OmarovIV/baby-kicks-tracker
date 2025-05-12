from datetime import datetime
from settings import get_pregnancy_start_date

def calculate_pregnancy_weeks(record_date_str):
    start_date_str = get_pregnancy_start_date()
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        record_date = datetime.strptime(record_date_str, "%Y-%m-%d")
        delta = record_date - start_date
        weeks = delta.days // 7
        days = delta.days % 7
        return f"{weeks} weeks {days} days"
    except Exception:
        return "N/A"
