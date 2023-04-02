from datetime import timezone
import datetime


if __name__ == "__main__":
    start_time = datetime.time(7,0)
    start_date = datetime.date(2001,2,3)
    print(datetime.datetime.combine(start_date, start_time))

    date_time = datetime.datetime.now(timezone.utc)

    utc_time = date_time.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    print(utc_timestamp)

    