#!/usr/bin/env python3

import nasne
from nasne import Nasne
import chinachu
from chinachu import Chinachu
import nachune
import pyrfc3339
from datetime import timedelta
import slack


def main():
    n = Nasne(nachune.nasne_address)
    c = Chinachu(nachune.chinachu_address)
    for np in n.conflict_programs():
        try:
            sid = np["serviceId"]
            start = pyrfc3339.parse(np["startDateTime"])
            duration = timedelta(seconds=np["duration"])
            title = Nasne.normalize(np["title"])
            cp = nachune.match_program(c, sid, start=start, duration=duration, title=title)
            c.reserve(cp["id"])
        except chinachu.DuplicatedReserveError as e:
            nachune.logger.info(e.message)
            slack.info("すでに予約されています", np, cp if cp else None)
        except nachune.NachuneError as e:
            nachune.logger.warning(e.message)
            slack.warning("該当する番組が見つかりませんでした", np)
        except nasne.NasneError as e:
            nachune.logger.error(e.message)
            slack.error(e.message, np)
        except chinachu.ChinachuError as e:
            nachune.logger.error(e.message)
            slack.error(e.message, np)
        else:
            nachune.logger.info(f"Successfully reserved: {title} (pid={np['id']}, sid={sid}, start={start.isoformat()}, duration={duration.isoformat()})")
            slack.success("録画予約しました", np, cp)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        nachune.logger.fatal(e)
