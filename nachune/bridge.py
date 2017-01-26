from datetime import datetime, timedelta
from chinachu.chinachu import Chinachu, JST
from .config import match_start_gap, match_end_gap, match_duration_gap, match_title_check
from .align import smith_waterman


class NachuneError(Exception):
    def __init__(self):
        self.message = ""


class PoorTitleMatchError(NachuneError):
    def __init__(self, t1: str, t2: str):
        self.message = f"Poor title match: {t1} and {t2}"
        self.title1 = t1
        self.title2 = t2


class NoMatchError(NachuneError):
    def __init__(self, title: str, sid: int, start: datetime, end: datetime):
        self.message = f"No matched title for {title} (sid={sid}, start={start.isoformat()}, end={end.isoformat()})"
        self.title = title
        self.sid = sid
        self.start = start
        self.end = end
        self.duration = end - start


def match_program(chinachu: Chinachu, sid: int, *, start: datetime, duration: timedelta=None, end: datetime=None, title: str="") -> dict:
    if duration is None and end is None:
        raise Exception("duration or end is required.")
    if duration is None:
        duration = end - start
    if end is None:
        end = start + duration

    schedule = chinachu.channel_schedule(sid)
    if not schedule:
        raise NoMatchError(title, sid, start, end)
    for p in schedule["programs"]:
        s = datetime.fromtimestamp(int(p["start"] / 1000), tz=JST())
        e = datetime.fromtimestamp(int(p["end"] / 1000), tz=JST())
        d = e - s
        if abs((start - s).total_seconds()) <= match_start_gap.total_seconds() \
            and abs((end - e).total_seconds()) <= match_end_gap.total_seconds() \
                and abs((duration - d).total_seconds()) <= match_duration_gap.total_seconds():
            if match_title_check:
                score = smith_waterman(title, p["title"])
                if score >= 10:
                    return p
                else:
                    raise PoorTitleMatchError(title, p["title"])
            else:
                return p
    raise NoMatchError(title, sid, start, end)
