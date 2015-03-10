from datetime import datetime, timedelta


class Singleton:
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwds):
        if self.instance is None:
            self.instance = self.cls(*args, **kwds)
        return self.instance


def modulo_timedelta(dt: datetime, td: timedelta) -> datetime:
    """
    Takes a datetime to perform modulo on and a timedelta.
    :returns: dt % td
    """
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return timedelta(seconds=((dt - today).total_seconds() % td.total_seconds()))


def floor_datetime(dt: datetime, td: timedelta) -> datetime:
    """
    Floors a datetime with interval zone td
    :returns: dt - dt % td
    """
    return dt - modulo_timedelta(dt, td)


def ceil_datetime(dt: datetime, td: timedelta) -> datetime:
    return floor_datetime(dt, td) + td
