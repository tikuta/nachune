import requests
import pyrfc3339
from datetime import timedelta
from collections import namedtuple


class NasneError(Exception):
    def __init__(self):
        self.message = ""


class HTTPError(NasneError):
    def __init__(self, status_code):
        self.message = f"HTTP error: {status_code}"
        self.status_code = status_code


class ResponseError(NasneError):
    def __init__(self, error_code):
        self.message = f"Response error: {error_code}"
        self.error_code = error_code


class Nasne:
    def __init__(self, address):
        self.address = address

    def reserved(self) -> [dict]:
        url = f"http://{self.address}:64220/schedule/reservedListGet?searchCriteria=0&filter=0&startingIndex=0&requestedCount=0&sortCriteria=0&withDescriptionLong=0&withUserData=0"
        res = requests.get(url)

        status_code = res.status_code
        if status_code != 200:
            raise HTTPError(status_code)

        d = res.json()
        error_code = d["errorcode"]
        if error_code != 0:
            raise ResponseError(error_code)

        return d["item"]

    def conflict_programs(self) -> [dict]:
        try:
            conflicts = [p for p in self.reserved() if p["conflictId"] != 0]
        except NasneError:
            return []

        r = []
        for i, p1 in enumerate(conflicts):
            t1 = pyrfc3339.parse(p1["startDateTime"])
            d1 = timedelta(seconds=p1["duration"])

            for j, p2 in enumerate(conflicts):
                if i >= j:
                    continue

                t2 = pyrfc3339.parse(p2["startDateTime"])
                d2 = timedelta(seconds=p2["duration"])

                latest_start = max(t1, t2)
                earliest_end = min(t1 + d1, t2 + d2)
                overlap = earliest_end - latest_start

                if overlap.total_seconds() > 0:
                    r.append(max(p1, p2, key=lambda p: p["conflictId"]))
        return r

    @staticmethod
    def normalize(s: str) -> str:
        PUA = namedtuple("PUA", ["src", "dst"])
        arr = [
            PUA(r'\ue0fd', '手'),
            PUA(r'\ue0fe', '字'),
            PUA(r'\ue0ff', '双'),
            PUA(r'\ue180', 'デ'),
            PUA(r'\ue182', '二'),
            PUA(r'\ue183', '多'),
            PUA(r'\ue184', '解'),
            PUA(r'\ue185', 'SS'),
            PUA(r'\ue18c', '映'),
            PUA(r'\ue18d', '無'),
            PUA(r'\ue190', '前'),
            PUA(r'\ue191', '後'),
            PUA(r'\ue192', '再'),
            PUA(r'\ue193', '新'),
            PUA(r'\ue194', '初'),
            PUA(r'\ue195', '終'),
            PUA(r'\ue196', '生'),
            PUA(r'\ue19c', '他')
        ]

        import re
        for p in arr:
            s = re.sub(p.src, "[" + p.dst + "]", s)
        s = re.sub(r'[\ue000-\uf8ff]', "", s)
        return s
