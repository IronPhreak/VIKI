import json

from yapsy.IPlugin import IPlugin

from main import logger


class PluginOne(IPlugin):
    def process(self):
        logger.info(__name__ + ": Detected")
        pass

    def task(self, query):
        s = str(query).split("|")
        Value = s[0]
        Content = s[1]
        data_store(Value, Content)
        # test8
        pass


def data_store(key_id, key_info):
    try:
        with open('Plugins/Phone/data.txt', 'r+') as f:
            data = json.load(f)
            data[key_id] = key_info
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        pass
    except ValueError:
        logger.error("Error in Phone store")
