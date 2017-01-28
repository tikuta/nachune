import requests
from nachune import slack_webhook_url
import json
import enum
from nasne import Nasne
import pyrfc3339
from datetime import timedelta, datetime
from chinachu.chinachu import JST


class NotifyLevel(enum.Enum):
    info = "#E0E0E0"
    success = "good"
    warning = "warning"
    error = "danger"


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


def post(level: NotifyLevel, message: str, np: dict, cp: dict):
    cp = cp if cp else {}

    emoji = ""
    if level is NotifyLevel.success:
        emoji = ":clock3:"
    elif level is NotifyLevel.warning:
        emoji = ":warning:"
    elif level is NotifyLevel.error:
        emoji = ":heavy_exclamation_mark:"

    data = {
        "attachments": [
            {
                "pretext": emoji + message,
                "color": level.value,
                "fallback": f"{level.name.upper()}: {message}",
                "fields": [__nasne2slack(np), __chinachu2slack(cp)] if len(cp) > 0 else [__nasne2slack(np)]
            }
        ]
    }
    if slack_webhook_url:
        requests.post(slack_webhook_url, data=json.dumps(data))


def info(message: str, np: dict, cp: dict=None):
    post(NotifyLevel.info, message, np, cp)


def success(message: str, np: dict, cp: dict=None):
    post(NotifyLevel.success, message, np, cp)


def warning(message: str, np: dict, cp: dict=None):
    post(NotifyLevel.warning, message, np, cp)


def error(message: str, np: dict, cp: dict=None):
    post(NotifyLevel.error, message, np, cp)