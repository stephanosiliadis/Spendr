from datetime import datetime, timedelta, date
from dateutil.parser import parse as date_parse


def parse_transaction_date(date_str: str) -> date:
    """
    Parse a date string for a transaction.

    Acceptable formats:
        - 'today' -> current date
        - 'yesterday' -> yesterday's date
        - any date string like '2026-03-11'

    Returns:
        datetime.date
    """
    if not date_str or date_str.strip() == "":
        return datetime.today().date()
    date_str = date_str.strip().lower()
    if date_str == "today":
        return datetime.today().date()
    elif date_str == "yesterday":
        return (datetime.today() - timedelta(days=1)).date()
    else:
        return date_parse(date_str).date()
