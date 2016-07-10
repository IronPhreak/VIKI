from yapsy.IPlugin import IPlugin

from main import logger


class PluginOne(IPlugin):
    def process(self):
        logger.info(__name__ + ": Detected")
        pass


def data_store(query):
    s = str(query).split("|")
    app = s[0]
    contact = s[1]
    message = s[2]
    with open('Plugins/Database/messages.txt', 'a') as f:
        f.write(app + "," + contact + "," + message + "\n")
    logger.info("Message Stored")
    pass
