import requests
from yapsy.IPlugin import IPlugin

from main import get_key, logger


class PluginOne(IPlugin):
    def process(self):
        logger.info(__name__ + ": Detected")
        pass

    def task(self, query):
        if str(query).split("|")[0].lower() == "store":
            from main import data_store
            data_store((str(query).split("|")[1]), str(query).split("|")[2])
        pass


def post(destination, text):
    try:
        # AutoRemote
        url = "https://autoremotejoaomgcd.appspot.com/sendmessage?key=" + get_key(
            destination) + "&message=VIKI=:=" + text
        requests.post(url=url)
    except Exception:
        logger.error("Error: in AutoRemote" + str(Exception))
