from datetime import datetime, tzinfo, time
from pytz import timezone

def get_content_list(soup_list):
    return list(filter(lambda f: f, map(lambda m: m.string, soup_list)))

def date_string_to_timestamp(year, month, day, time_str):
    """
    example parameters (2019, 1, 31, "9:45 PM MST")
    """
    TZ_OFFSET_MAP = {
        'EDT': 'US/Eastern',
        'EST': 'US/Eastern',
        'CDT': 'US/Central',
        'CST': 'US/Central',
        'MDT': 'US/Mountain',
        'MST': 'US/Mountain',
        'PDT': 'US/Pacific',
        'PST': 'US/Pacific'
    }
    year = int(year)
    month = int(month)
    day = int(day)
    time_arr = time_str.split(' ')
    assert len(time_arr) == 3
    time = datetime.strptime(' '.join(time_arr[:2]), '%I:%M %p')
    tz = TZ_OFFSET_MAP[time_arr[2]]
    dt = datetime(year=year, month=month, day=day, hour=time.hour, minute=time.minute)
    local_dt = timezone(tz).localize(dt)
    return int(local_dt.timestamp())