import wikipedia
from yapsy.IPlugin import IPlugin

from main import logger


class PluginOne(IPlugin):
    def process(self):
        logger.info(__name__ + ": Detected")
        pass

    def task(self, query):
        q = str(query).split(' ')
        if q[0] == "summary":
            query = str(query).replace(q[0], "")
            return summary(query)
        pass


def choice(cmd):
    query = str(cmd).split(" ")
    print(query[0])
    if query[0] == "Summary":
        logger.info("Getting Summary")
        query.remove(query[0])
        return summary(query)


def summary(query):
    x = wikipedia.summary(query, sentences=1)
    return x
