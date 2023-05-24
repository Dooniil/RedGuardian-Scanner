import datetime
import time


class TimerError(Exception):
    pass


class TimeInfoManager:
    def __init__(self):
        self._start_time = None
        self._start_datetime = None
        self._exec_time = None
        self._end_datetime = None

    def start(self):
        if self._start_time is not None:
            raise TimerError(f"Таймер уже работает. Используйте .stop() чтобы его остановить")

        self._start_time = time.perf_counter()
        self._start_datetime = datetime.datetime.utcnow().isoformat(sep=' ', timespec='seconds')

    def stop(self):
        if self._start_time is None:
            raise TimerError(f"Таймер не работает. Используйте .start() для его запуска")

        self._exec_time = time.perf_counter() - self._start_time
        self._start_time = None
        self._end_datetime = datetime.datetime.utcnow().isoformat(sep=' ', timespec='seconds')

    @property
    def exec_time(self):
        td = datetime.timedelta(seconds=self._exec_time)
        return str(datetime.timedelta(seconds=td.seconds))

    @property
    def exec_date(self):
        return self._start_datetime, self._end_datetime
