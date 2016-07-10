import json
import logging
import threading
import time
import urllib
from subprocess import Popen
from sys import exit
from urllib import request

from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor
from yapsy.PluginManager import PluginManager

logging.basicConfig(level=logging.DEBUG,
                    filename='debug.log',
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='w')
logger = logging.getLogger(__name__)


class Server(WebSocketServerProtocol):
    def onConnect(self, request):
        logger.info("Client connecting: {}".format(request.peer))

    def onOpen(self):
        logger.info("WebSocket connection open.")

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {}".format(reason))

    def onMessage(self, payload, isBinary):
        # Analyse the message
        logger.info("Incomming Message: " + payload.decode())
        source = str(payload.decode()).split("|")[0]
        message = str(payload.decode()).split("|")[1]
        logger.info("Source: " + source)
        logger.info("Query: " + message)

        # Query it
        answer = operator(message)
        output(answer)


def operator(query):
    try:
        q = query.split(' ')
        logger.info("Querying Plugins: " + q[0])

        # Create plugin manager object
        simplepluginmanager = PluginManager()

        # Gain plugin information
        simplepluginmanager.setPluginPlaces(["Plugins"])
        simplepluginmanager.collectPlugins()
        for pluginInfo in simplepluginmanager.getAllPlugins():
            if str(pluginInfo.name).lower() == q[0].lower():
                logger.info("")
                return pluginInfo.plugin_object.task(query)
    except Exception as exc:
        logger.error(exc.args)
        return "Error in operator"


def detect_plugins():
    logger.info("Detecting Plugin")
    # Create plugin manager object
    simplepluginmanager = PluginManager()

    # Gain plugin information
    simplepluginmanager.setPluginPlaces(["Plugins"])
    simplepluginmanager.collectPlugins()

    for pluginInfo in simplepluginmanager.getAllPlugins():
        p = threading.Thread(target=pluginInfo.plugin_object.process())
        logging.info("Detected Plugin" + pluginInfo.name)
        p.start()


def get_key(key_id):
    try:
        with open('Keys.txt', 'r') as f:
            data = json.load(f)
            return data[key_id]
    except ValueError:
        logger.error("Error in get_key")


def output(text):
    try:
        print(text)
        logger.info("Output: text")
        # AutoRemote
        from Plugins.AutoRemote.plugin import post
        post(text)
    except Exception as exc:
        logger.error(exc.args)
        pass


def data_store(key_id, key_info):
    try:
        with open('Keys.txt', 'r+') as f:
            data = json.load(f)
            data[key_id] = key_info
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        pass
    except ValueError:
        logger.error("Error in data store")


def version_check():
    while True:
        try:
            # Wait for 1 minute
            time.sleep(60)
            # Checking current version
            logger.info("checking for updates")
            version = get_key('version')
            logger.info("Current version: " + version)

            # Checking for update
            url = "http://ironphreak.com/viki/data.txt"
            urllib.request.urlretrieve(url, "ver.txt")
            with open("ver.txt", 'r') as info:
                ver = json.load(info)
            updated = ver['version']
            logger.info("Latest version: " + updated)

            # Comparing version
            if updated > version:
                logger.info("Update Available")
                output("Update Available")
                from updater import download_update
                Popen(download_update(updated))
                exit("exit for updating files")
        except ValueError:
            logger.exception("Error in Version Check")
            pass


if __name__ == "__main__":
    # Version Checking
    t = threading.Thread(target=version_check)
    logging.info("Starting thread: Version_Checking")
    t.start()

    # Plugins
    detect_plugins()

    logger.info("VIKI Loaded: Version " + get_key("version"))
    logger.info("Server started")

    # Start HTTP server
    from autobahn.twisted.websocket import WebSocketServerFactory

    factory = WebSocketServerFactory()
    factory.protocol = Server
    reactor.listenTCP(9000, factory)
    output("Server is up")
    reactor.run()
