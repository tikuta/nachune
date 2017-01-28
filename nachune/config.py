import logging
import os
from configparser import ConfigParser
from datetime import timedelta

__config = ConfigParser()
__config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), "nachune.ini"))


log_handler = logging.FileHandler(__config["general"]["log"])
log_handler.setLevel(logging.INFO)
log_handler.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("nachune")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

nasne_address = __config["general"]["nasne"]
chinachu_address = __config["general"]["chinachu"]

match_start_gap = timedelta(minutes=__config["match"].getint("start"))
match_end_gap = timedelta(minutes=__config["match"].getint("end"))
match_duration_gap = timedelta(minutes=__config["match"].getint("duration"))
match_title_check = __config["match"].getboolean("title")

slack_webhook_url = __config["notify"]["slack"]