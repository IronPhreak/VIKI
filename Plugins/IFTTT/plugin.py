import requests
from yapsy.IPlugin import IPlugin

from main import get_key, logger


class PluginOne(IPlugin):
    def process(self):
        logger.info(__name__ + ": Detected")
        pass

    def task(self, query):
        pass


def post(event, value1, value2, value3):
    try:
        url = "https://maker.ifttt.com/trigger/" + event + "/with/key/" + get_key("IFTTT")
        payload = {}
        if value1 is not None:
            payload = {"value1": value1}
        if value2 is not None:
            payload = {"value2": value2}
        if value3 is not None:
            payload = {"value3": value3}
        requests.post(url=url, data=payload)
    except Exception:
        logger.error("Error in IFTTT: " + str(Exception))
