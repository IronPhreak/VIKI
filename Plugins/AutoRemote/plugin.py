import requests
from yapsy.IPlugin import IPlugin

from main import get_key, logger


class PluginOne(IPlugin):
    def process(self):
        logger.info(__name__ + ": Detected")
        pass

    def task(self, query):
        pass


def post(text):
    try:
        # AutoRemote
        url = "https://autoremotejoaomgcd.appspot.com/sendmessage?key=" + get_key(
            "AutoRemote") + "&message=VIKI=:=" + text
        requests.post(url=url)
    except Exception:
        logger.error("Error: in AutoRemote" + str(Exception))
