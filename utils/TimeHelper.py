from datetime import datetime, timezone


def get_current_timestamp_utc() -> str:
    current_utc_date: datetime = datetime.now(tz=timezone.utc)

    current_utc_date_formatted: str = current_utc_date.strftime('%Y-%m-%dT%H-%M-%S-%f')[:-3]
    
    return current_utc_date_formatted
    