from yapsy.IPlugin import IPlugin

from main import logger, data_store


class PluginOne(IPlugin):
    def process(self):
        logger.info(__name__ + ": Detected")
        pass

    def task(self, query):
        s = str(query).split(":")
        Value = s[0]
        logger.info("Value: " + Value)
        Content = s[1]
        logger.info("Content: " + Content)
        data_store(Value, Content)
        # test8
        pass
