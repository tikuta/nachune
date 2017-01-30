import requests
from nachune import slack_webhook_url
import json
import enum
from nasne import Nasne
import pyrfc3339
from datetime import timedelta, datetime
from chinachu.chinachu import JST
from collections import namedtuple


Attachments = namedtuple("Attachments", ["color", "emoji"])


class NotifyLevel(enum.Enum):
    info = Attachments(color="#E0E0E0", emoji="")
    success = Attachments(color="good", emoji=":clock3:")
    warning = Attachments(color="warning", emoji=":warning:")
    error = Attachments(color="danger", emoji=":heavy_exclamation_mark:")
    fatal = Attachments(color="danger", emoji=":heavy_exclamation_mark::heavy_exclamation_mark:")


def __nasne2slack(np: dict) -> dict:
    title = Nasne.normalize(np["title"])
    start = pyrfc3339.parse(np["startDateTime"])
    duration = timedelta(seconds=np["duration"])
    end = start + duration
    field = {
        "title": "Nasne",
        "value": f"{title} ({np['channelName']}, {start.strftime('%m/%d %H:%M')} - {end.strftime('%H:%M')})",
        "short": False
    }
    return field


def __chinachu2slack(cp: dict) -> dict:
    start = datetime.fromtimestamp(int(cp["start"] / 1000), tz=JST())
    end = datetime.fromtimestamp(int(cp["end"] / 1000), tz=JST())
    field = {
        "title": "Chinachu",
        "value": f"{cp['title']} ({cp['channel']['name']}, {start.strftime('%m/%d %H:%M')} - {end.strftime('%H:%M')})",
        "short": False
    }
    return field


def post(level: NotifyLevel, message: str, *, text: str=None, fields: [dict]=None):
    if not slack_webhook_url:
        return

    payload = {
        "attachments": [
            {
                "pretext": level.value.emoji + message,
                "color": level.value.color,
                "fallback": f"{level.name.upper()}: {message}",
                "text": text if text else "",
                "fields": fields if fields else []
            }
        ]
    }

    requests.post(slack_webhook_url, data=json.dumps(payload))


def info(message: str, np: dict, cp: dict):
    post(NotifyLevel.info, message, fields=[__nasne2slack(np), __chinachu2slack(cp)])


def success(message: str, np: dict, cp: dict):
    post(NotifyLevel.success, message, fields=[__nasne2slack(np), __chinachu2slack(cp)])


def warning(message: str, np: dict):
    post(NotifyLevel.warning, message, fields=[__nasne2slack(np)])


def error(message: str, np: dict=None, cp: dict=None):
    fields = []
    if np:
        fields.append(__nasne2slack(np))
    if cp:
        fields.append(__chinachu2slack(cp))

    post(NotifyLevel.error, message, fields=fields)


def fatal(message: str):
    post(NotifyLevel.fatal, message)
