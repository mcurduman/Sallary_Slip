from datetime import date

def validate_date_range(start_date: date | None, end_date: date | None) -> bool:
    if end_date and not start_date:
        return False
    elif start_date and not end_date:
        return True
    return start_date <= end_date