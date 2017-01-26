from datetime import timedelta, tzinfo
import requests


class ChinachuError(Exception):
    def __init__(self):
        self.message = ""


class DuplicatedReserveError(ChinachuError):
    def __init__(self, pid: str):
        self.message = f"Duplicated reserve: {pid}"
        self.pid = pid


class HTTPError(ChinachuError):
    def __init__(self, status_code):
        self.message = f"HTTP error: {status_code}"
        self.status_code = status_code


class JST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)

    def tzname(self, dt):
        return "JST"

    def dst(self, dt):
        return timedelta()


class Chinachu:
    def __init__(self, address):
        self.address = address

    def schedule(self) -> [dict]:
        url = f"http://{self.address}/api/schedule.json"
        res = requests.get(url)
        status_code = res.status_code
        if status_code != 200:
            raise HTTPError(status_code)
        return res.json()

    def channel_schedule(self, sid: int) -> dict:
        for c in self.schedule():
            if c["sid"] == sid:
                return c

    def reserve(self, pid: str):
        url = f"http://{self.address}/api/program/{pid}.json"
        res = requests.put(url)
        status_code = res.status_code
        if status_code == 409:
            raise DuplicatedReserveError(pid)
        if status_code != 200:
            raise HTTPError(status_code)
